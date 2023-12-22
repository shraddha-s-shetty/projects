#import webdriver
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://www.amazon.in/")

options = driver.find_element(By.XPATH, '//*[@id="searchDropdownBox"]')

print("Enter the category you need to search from below options: ",options.text)

category = input("Enter value to search: ")
options.send_keys(category)

search = driver.find_element(By.XPATH ,'//*[@id="twotabsearchtextbox"]')

search_val = input("Enter the search item and its features: ")
search.send_keys(search_val)

search.submit()

dicts = {}
def html_parser(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all(class_="a-section a-spacing-small puis-padding-left-micro puis-padding-right-micro")
    for product in products:
        try:
            print("""next line """)
            brand = product.find('span',class_="a-size-base-plus a-color-base")
            print("I am brand", brand.text)
            name = product.find('span',class_="a-size-base-plus a-color-base a-text-normal")
            print("I am name", name.text)
            price = product.find('span',class_="a-price-whole")
            print("I am price", price.text)
            mrp = product.select('[aria-hidden="true"]')
            print("I am mrp", mrp[-1].text)
            dicts[name.text] = f'["Brand": {brand.text}, "Price": {price.text}, "MRP": {mrp[-1].text}]'
        except Exception as error:
            continue
    #print(dicts)
    return dicts

def generate_xpath(element):
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

def get_next_button(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    pattern = r"s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"
    matching_a_elements = soup.find_all('a', class_=re.compile(pattern))

    for a_element in matching_a_elements:
        xpath = generate_xpath(a_element)
        return xpath

current_page = 1
while True:
    if current_page == 10:
        break
    time.sleep(10)
    html_content = driver.page_source
    html_parser(html_content)
    next_button_xpath = str(get_next_button(html_content))

    try:
        current_url = driver.current_url
        print("Current URL:", current_url)
        wait = WebDriverWait(driver, 20)
        next_button = wait.until(EC.visibility_of_element_located((By.XPATH, next_button_xpath)))
    except Exception as e:
        next_button_xpath = str(str(next_button_xpath).replace('a[3]', 'a[4]'))
        wait = WebDriverWait(driver, 20)
        next_button = wait.until(EC.visibility_of_element_located((By.XPATH, next_button_xpath)))
        pass

    if next_button.is_enabled():
        # Click the next button to go to the next page
        next_button.click()
        current_page += 1
    else:
        break
a = len(dicts)
print(a)
df = pd.DataFrame(dicts,index=[0,a])
print(df)
excel_file = 'data.xlsx'
df.to_excel(excel_file, index=True)
print("DataFrame exported to Excel successfully.")
    


driver.close()
