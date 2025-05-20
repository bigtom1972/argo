from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import logging

# Set up logging for debugging
logging.basicConfig(filename="scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")  # Required for Linux
chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid memory issues

# Specify ChromeDriver path
#chromedriver_path = "/home/robot/chromedriver"  # Update if path differs
#service = Service(chromedriver_path, log_path="chromedriver.log")
driver = None
try:
    # Initialize WebDriver
    driver = webdriver.Chrome( options=chrome_options)
    logging.info("WebDriver initialized successfully")

    # Navigate to the page
    url = "https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/"
    driver.get(url)
    logging.info(f"Navigated to {url}")

    # Open CSV file to save data
    with open("lottery_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Write header (adjust based on actual table columns after inspection)
        writer.writerow(["Issue", "Date", "Red Balls", "Blue Ball", "Sales", "Prize Pool", "1st Prize Winners", "1st Prize Amount"])

        page_count = 0
        while True:
            try:
                # Wait for the table to load
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "table"))
                )
                logging.info(f"Table found on page {page_count + 1}")

                # Find the table (update to specific class if needed, e.g., By.CLASS_NAME, "kj_table")
                table = driver.find_element(By.TAG_NAME, "table")
                rows = table.find_elements(By.TAG_NAME, "tr")

                # Extract table data
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    row_data = [col.text.strip().replace("\n", ":") for col in cols]
                    if row_data:  # Skip empty rows
                        logging.info(f"Row data: {row_data}")
                        writer.writerow(row_data)
                        print(row_data)

                # Check for "Next" button
                try:
                    next_button = driver.find_element(By.CLASS_NAME, "layui-laypage-next")
                    if not next_button.is_enabled() or "disabled" in next_button.get_attribute("class"):
                        logging.info("No more pages to scrape")
                        break

                    # Scroll to the button to ensure it's clickable
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(0.5)  # Brief pause to ensure scroll completes

                    # Click the "Next" button
                    next_button.click()
                    logging.info(f"Clicked 'Next' button for page {page_count + 2}")

                    # Wait for the new page's table to load
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.TAG_NAME, "table"))
                    )
                    page_count += 1

                except Exception as e:
                    logging.info(f"No next button found or pagination ended: {str(e)}")
                    break

            except Exception as e:
                logging.error(f"Error during table scraping on page {page_count + 1}: {str(e)}")
                break

except Exception as e:
    logging.error(f"WebDriver error: {str(e)}")
    print(f"Error: {str(e)}")

finally:
    driver.quit()
    logging.info("WebDriver closed")