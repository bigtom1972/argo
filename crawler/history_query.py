
# import requests
# from bs4 import BeautifulSoup

# url = "https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/"
# response = requests.get(url)
# soup = BeautifulSoup(response.content, "html.parser")

# # Find the table (inspect the page to get the correct class or ID)
# table = soup.find("table")  # Adjust based on actual HTML
# rows = table.find_all("tr")

# for row in rows:
#     cols = row.find_all("td")
#     cols = [col.text.strip() for col in cols]
#     print(cols)  # Process or save the data as needed


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Path to ChromeDriver (update with your path if not in PATH)
# service = Service("/path/to/chromedriver")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)  # Use service=service if specifying path

try:
    # Navigate to the page
    url = "https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/"
    driver.get(url)

    # Wait for the table to load (adjust timeout and selector as needed)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )

    # Find the table (inspect the page to confirm the table's class or ID)
    table = driver.find_element(By.TAG_NAME, "table")  # Update with specific class/ID if available
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Extract table data
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        row_data = [col.text.strip() for col in cols]
        if row_data:  # Skip empty rows
            print(row_data)

    # Optional: Handle pagination if the table spans multiple pages
    while True:
        try:
            # Find the "Next" button (inspect the page for the correct selector)
            next_button = driver.find_element(By.XPATH, "//a[contains(text(), '下一页')]")  # Adjust XPath
            if "disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
            table = driver.find_element(By.TAG_NAME, "table")
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                row_data = [col.text.strip() for col in cols]
                if row_data:
                    print(row_data)
        except:
            break

finally:
    # Close the browser
    driver.quit()