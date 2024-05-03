# import requests
# from bs4 import BeautifulSoup
# import json
# import os

# vc_websites = [
#     'https://www.accel.com', 'https://www.a16z.com', 'https://www.greylock.com',
#     'https://www.sequoiacap.com', 'https://www.indexventures.com',
#     'https://www.kpcb.com', 'https://www.lsvp.com', 'https://www.matrixpartners.com',
#     'https://www.500.co', 'https://www.sparkcapital.com', 'https://www.insightpartners.com'
# ]


# def clean_vc_name(title):
#     common_unwanted = {'home', 'welcome'}

#     if '|' in title:
#         parts = [part.strip() for part in title.split('|')]
#     elif '-' in title:
#         parts = [part.strip() for part in title.split('-')]
#     elif '–' in title: 
#         parts = [part.strip() for part in title.split('–')]
#     else:
#         return title.strip()

#     parts = [part for part in parts if part.lower() not in common_unwanted]

#     return parts[0] if parts else title.strip()

# def scrape_vc_info(url):
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#         }
#         response = requests.get(url, headers=headers)
#         response.raise_for_status() 

#         soup = BeautifulSoup(response.text, 'html.parser')

#         vc_name = clean_vc_name(soup.title.text) if soup.title else 'VC Name Not Found'
        
#         contact_info = soup.find('footer') or soup.find('div', class_='contact')
#         contacts = contact_info.get_text(strip=True) if contact_info else 'Contact Info Not Found'

#         industries_section = soup.find(string=lambda text: text and 'industries' in text.lower())
#         industries = industries_section.find_next('ul').get_text(',') if industries_section and industries_section.find_next('ul') else 'Industries Not Found'

#         investment_rounds = 'Investment Rounds Information Not Found'

#         vc_info = {
#             'VC Name': vc_name,
#             'Contacts': contacts,
#             'Industries': industries,
#             'Investment Rounds': investment_rounds
#         }

#         return vc_info

#     except Exception as e:
#         return {'error': str(e)}

# folder_path = 'Data'
# os.makedirs(folder_path, exist_ok=True)

# for url in vc_websites:
#     vc_info = scrape_vc_info(url)
#     domain_name = url.split('//')[1].split('/')[0]
#     file_path = os.path.join(folder_path, f'{domain_name}.json')
#     with open(file_path, 'w') as file:
#         json.dump(vc_info, file, indent=4)

# print("Scraping completed and data saved in 'Data' folder.")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import os
import time

vc_websites = [
    'https://www.accel.com', 'https://www.a16z.com', 'https://www.greylock.com',
    'https://www.benchmark.com', 'https://www.sequoiacap.com', 'https://www.indexventures.com',
    'https://www.kpcb.com', 'https://www.lsvp.com', 'https://www.matrixpartners.com',
    'https://www.500.co', 'https://www.sparkcapital.com', 'https://www.insightpartners.com'
]

contact_keywords = ['connect', 'contact-us', 'get-in-touch', 'contact', 'global-presence']


def clean_vc_name(title):
    common_unwanted = {'home', 'welcome'}

    if '|' in title:
        parts = [part.strip() for part in title.split('|')]
    elif '-' in title:
        parts = [part.strip() for part in title.split('-')]
    elif '–' in title: 
        parts = [part.strip() for part in title.split('–')]
    else:
        return title.strip()

    parts = [part for part in parts if part.lower() not in common_unwanted]

    return parts[0] if parts else title.strip()


def scrape_vc_info(url):
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        time.sleep(5) 

        found = False
        for keyword in contact_keywords:
            elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{keyword}')]")
            for element in elements:
                if element.tag_name in ['a', 'button']:
                    try:
                        element.click()
                        time.sleep(3)  
                        found = True
                        break
                    except:
                        continue
            if found:
                break

        contact_html = driver.page_source
        contact_soup = BeautifulSoup(contact_html, 'html.parser')
        contacts = contact_soup.get_text(strip=True)

        soup = BeautifulSoup(contact_html, 'html.parser')
        vc_name = clean_vc_name(soup.title.text) if soup.title else 'VC Name Not Found'
        industries_section = soup.find(string=lambda text: text and 'industries' in text.lower())
        industries = industries_section.find_next('ul').get_text(',') if industries_section and industries_section.find_next('ul') else 'Industries Not Found'
        investment_rounds = 'Investment Rounds Information Not Found'

        vc_info = {
            'VC Name': vc_name,
            'Contacts': contacts,
            'Industries': industries,
            'Investment Rounds': investment_rounds
        }

        return vc_info

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return {'error': str(e)}
    finally:
        if driver:
            driver.quit()

folder_path = 'Data'
os.makedirs(folder_path, exist_ok=True)

results = {}
for url in vc_websites:
    vc_info = scrape_vc_info(url)
    domain_name = url.split('//')[1].split('/')[0]
    file_path = os.path.join(folder_path, f'{domain_name}.json')
    with open(file_path, 'w') as file:
        json.dump(vc_info, file, indent=4)
    results[url] = vc_info

print("Scraping completed and data saved in 'Data' folder.")
