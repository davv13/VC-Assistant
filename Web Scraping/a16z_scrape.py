from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors') 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
url = 'https://a16z.com/about/'
driver.get(url)

try:
    wait = WebDriverWait(driver, 20)

    left_appeared_div = wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'left.is-appeared')))
    h2_heading = left_appeared_div.find_element(By.TAG_NAME, 'h2').text
    paragraphs = left_appeared_div.find_elements(By.TAG_NAME, 'p')
    p_texts = [p.text for p in paragraphs]

    animated_contents = driver.find_elements(By.CSS_SELECTOR, "div.right.animated-slide-content")
    animated_texts = []
    for content in animated_contents:
        paragraphs = content.find_elements(By.TAG_NAME, 'p')
        paragraph_texts = [paragraph.text for paragraph in paragraphs if paragraph.text]
        animated_texts.extend(paragraph_texts)

    
    about_content = f" {h2_heading}\n\n" + "\n\n".join(p_texts)
    about_content = "\n\n".join(animated_texts)

    data_directory = 'data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    markdown_file = os.path.join(data_directory, 'a16z_about.md')

    with open(markdown_file, 'a', encoding='utf-8') as file:
        file.write(about_content)

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()



