# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://www.amazon.in/")

options = driver.find_element(By.XPATH, '//*[@id="searchDropdownBox"]')

print("Enter the category you need to search from below options: ",options.text)

category = input("Enter value to search: ")
options.send_keys(category)

search = driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')

search_val = input("Enter the search item and its features: ")
search.send_keys(search_val)

search.submit()

dicts = {}
def extract_information():
    items = driver.find_elements(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[1]')  
    for item in items:
        #item = driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[6]')
        sale = item.find_element(By.XPATH,'//*[@id="BLACK_FRIDAY-label"]/span/span')
        if sale:
            title = item.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[6]/div/div/div/div/div[2]/div[1]/div/h2/span').text
            actualprice = item.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[6]/div/div/div/div/div[2]/div[3]/div[2]/a/div/span[2]/span[2]').text
            mrp = item.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[6]/div/div/div/div/div[2]/div[3]/div[2]/a/span/span[2]/span[2]').text
            off_percent = item.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[6]/div/div/div/div/div[2]/div[3]/div[2]/span[2]')
            dicts[title] = {'actualprice':actualprice,'mrp':mrp,'off_percent':off_percent}
        # Process or store the information as needed
    print(dicts)

extract_information()
current_page = 2
while True:
    driver.get(f"https://www.amazon.in/s?k={search_val}&i={category}&page={current_page}")

    extract_information()
    next_button = driver.find_element(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[62]/div/div/span/a[3]')  # Replace with the actual XPath of the next button
    if current_page == 20:
        print("Surfed 20 pages I am quitting now")
        print(dicts)
        driver.quit()

    if next_button.is_enabled():
        # Click the next button to go to the next page
        next_button.click()
        current_page += 1
    else:
        # No next page available, break out of the loop
        driver.quit()
        break
    driver.quit()


time.sleep(120)










driver.service.stop()




