from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import modin.pandas as pd

# Setup selenium object for Brave browser
options = Options()
PATH_TO_BINARY = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
options.binary_location = PATH_TO_BINARY
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options = options)

# Navigate to page
driver.get("https://bizfileonline.sos.ca.gov/search/business")

# Locate search bar and search for 'test'
search = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div/main/div/div[2]/div[1]/input")
search.send_keys('test')

# Wait until 'Advanced Settings' button is clickable
try:
  wait = WebDriverWait(driver, 10)
  element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[1]/div/main/div/div[2]/div[2]/button")))
except Exception as e:
  print(e)
  driver.quit()

# Locate and hit 'Enter' on 'Advanced Settings' button
advanced_settings = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div/main/div/div[2]/div[2]/button")
advanced_settings.send_keys("")
advanced_settings.send_keys(Keys.ENTER)

# Wait until dropdown is clickable
try:
  wait = WebDriverWait(driver, 10)
  element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='field-STATUS_ID']")))
except Exception as e:
  print(e)
  driver.quit()

# Locate and input 'Active' into dropdown
dropdown = driver.find_element_by_xpath("//*[@id='field-STATUS_ID']")
dropdown.send_keys("")
Select(dropdown).select_by_value("1")

# Wait until 'Search' button is clickable
try:
  wait = WebDriverWait(driver, 10)
  element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[1]/div/main/div/div[2]/div[2]/div/div/div/div[7]/div/button[1]")))
except Exception as e:
  print(e)
  driver.quit()

# Locate 'Search' button and hit 'Enter'
search_advanced = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div/main/div/div[2]/div[2]/div/div/div/div[7]/div/button[1]")
search_advanced.send_keys("")
search_advanced.send_keys(Keys.ENTER)

# Wait for search results to load
try:
  wait = WebDriverWait(driver, 60)
  table = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[1]/div/main/div[2]/table")))
except Exception as e:
  print(e)
  driver.quit()

# Extract page html from present page
html = driver.page_source

# Parse html with BeautifulSoup
soup = BeautifulSoup(html)
soup_table = soup.find("table")
table = pd.read_html(str(soup_table))

# Export table with pandas
table.to_csv('out.csv', index=False)

driver.quit()