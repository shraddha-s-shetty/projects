import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

data_dicts = {}

class AmazonScraper:
    def __init__(self,url):
        self.driver = self.setup_driver(url)
        

    def setup_driver(self,url):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        return driver

    def input_category(self):
        options_element = self.driver.find_element(By.XPATH, '//*[@id="searchDropdownBox"]')
        print("Enter the category you need to search from below options: ", options_element.text)
        category = input("Enter value to search: ")
        options_element.send_keys(category)

    def input_search_query(self):
        search_element = self.driver.find_element(By.XPATH ,'//*[@id="twotabsearchtextbox"]')
        search_val = input("Enter the search item and its features: ")
        search_element.send_keys(search_val)
        search_element.submit()

    def html_parser(self):
        products = self.driver.find_elements(By.XPATH,"//div[@data-component-type='s-search-result']")
        for product in products:
            try:
                brand = product.find_element(By.XPATH,".//h2")
                name = product.find_element(By.XPATH,".//h2/a")
                price = product.find_element(By.XPATH,'.//span[@class="a-price"]')
                mrp = product.find_element(By.XPATH,'.//span[@class="a-price a-text-price"]')
                
                data_dicts[name.text] = {
                    "Brand": brand.text,
                    "Price": price.text,
                    "MRP": mrp.text
                }
                print(f"Scraping watch details for brand {brand.text}")
            except Exception as error:
                #print(f"{error}: {product}")
                continue
        
    def generate_xpath(self, element):
        elements = []
        while element.parent is not None:
            parent = element.parent
            siblings = parent.find_all(element.name, recursive=False)
            if len(siblings) == 1:
                elements.insert(0, f"{element.name}")
            else:
                index = siblings.index(element) + 1
                elements.insert(0, f"{element.name}[{index}]")
            element = parent
        return '/' + '/'.join(elements)

    def get_next_button(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        pattern = r"s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"
        matching_a_elements = soup.find_all('a', class_=re.compile(pattern))
        for a_element in matching_a_elements:
            xpath = self.generate_xpath(a_element)
            return xpath

    # def send_item_selections(self):

    #     brands_element = self.driver.find_element(By.ID,"brandsRefinements")
    #     print("I am brand list:", brands_element)
    #     brands_dict = {}
    #     ul_element = brands_element.find_element(By.XPATH,".//ul")  
    #     li_elements = ul_element.find_elements(By.XPATH,".//li")
    #     print("ul_element",ul_element)
    #     print("li_elements",li_elements)
    #     condition = list(map(str.strip,input(f"Input the Brands you need ex-(Titan,Casio): ").split(',')))
    #     for li_element in li_elements:
    #         label = li_element.text
    #         if label in condition:
    #             li_element.click()
            
    #     price_list = self.driver.find_elements(By.ID,"priceRefinements")
    #     price_dicts = {}
    #     for item in price_list:
    #         ul_element = item.find_element(By.XPATH,".//ul")  
    #         li_elements = ul_element.find_elements(By.TAG_NAME,".li")

    #         condition = list(map(str.strip,input(f"Input the price you need ex-(₹5,000 - ₹10,000): ").split(',')))
    #         for li_element in li_elements:
    #             label = li_element.text
    #             if label in condition:
    #                 li_element.click()




    def scrape_multiple_pages(self, num_pages=30):
        current_page = 1
        while current_page <= num_pages:
            time.sleep(10)
            html_content = self.driver.page_source
            #self.send_item_selections()
            self.html_parser()
            next_button_xpath = self.get_next_button(html_content)
            try:
                current_url = self.driver.current_url
                print(current_url)
                wait = WebDriverWait(self.driver, 10)
                next_button = wait.until(EC.visibility_of_element_located((By.XPATH, next_button_xpath)))
                next_button.click()
                current_page += 1
            except Exception as e:
                if next_button_xpath == None:
                    break
                next_button_xpath = next_button_xpath.replace('a[3]', 'a[4]')
                wait = WebDriverWait(self.driver, 10)
                next_button = wait.until(EC.visibility_of_element_located((By.XPATH, next_button_xpath)))
                if next_button.is_enabled():
                    next_button.click()
                    current_page += 1
                else:
                    break

    def export_to_excel(self, excel_file='data.xlsx'):
        df = pd.DataFrame.from_dict(data_dicts, orient='index', columns=["Brand", "Price", "MRP"])
        df.index.name = "Name"
        df.to_excel(excel_file, index=True)
        print(f"DataFrame exported to {excel_file} successfully.")

    def close_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = AmazonScraper("https://www.amazon.in")
    scraper.input_category()
    scraper.input_search_query()
    scraper.scrape_multiple_pages()
    scraper.export_to_excel('laptop_16gb.xlsx')
    scraper.close_driver()
