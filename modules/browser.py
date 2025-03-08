from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def search_google(query):
    print(f"Searching Google for {query}...")
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    search_box = driver.find_element("name", "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)