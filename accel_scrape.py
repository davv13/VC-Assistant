from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors') 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
url = 'https://www.accel.com/relationships'
driver.get(url)
time.sleep(5)


try:
    wait = WebDriverWait(driver, 20)

    load_more_button = driver.find_element(By.CLASS_NAME, 'load-more-button')
    load_more_button.click()
    time.sleep(15)

    items = driver.find_elements(By.CSS_SELECTOR, "div.full-list---new.w-dyn-items > div.w-dyn-item")
    companies_data = []
    
    for item in items:
        company_name_script = """
            var companyNameDiv = arguments[0].querySelector('div.relationships-table---company-name div');
            return companyNameDiv ? companyNameDiv.textContent.trim() : "Not Found";
            """
        company_name = driver.execute_script(company_name_script, item)

        investment_round_element = item.find_element(By.CSS_SELECTOR, "div.text-block-2")
        investment_round = investment_round_element.text if investment_round_element else "Not Found"
        
        investment_year = ""
        try:
            investment_year_element = investment_round_element.find_element(By.XPATH, "following-sibling::div")
            investment_year = investment_year_element.text if investment_year_element else ""
        except Exception as e:
            print(f"Could not find investment year due to: {e}")
        
        investment_info = f"{investment_round} {investment_year}".strip()
        
        try:
            founders_info_elements = item.find_elements(By.CSS_SELECTOR, "div.relationships---founders.w-richtext p")
            founders_info = ", ".join([founder.text for founder in founders_info_elements if founder.text])
        except:
            founders_info = "Not Found"
        try:
            short_description = item.find_element(By.CSS_SELECTOR, "div.short-description.w-richtext p").text
        except:
            short_description = "Not Found"

        company_data = {
            'company_name': company_name,
            'investment_info': investment_info,
            'founders_info': founders_info,
            'short_description': short_description
        }
        companies_data.append(company_data)

    for company in companies_data:
        print(company)

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
