import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def sanitize_filename(title):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '_')
    return title.strip().strip('.')

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https'] and parsed.netloc == base_domain

def ends_with_keywords(url, keywords):
    parsed = urlparse(url)
    path = parsed.path.lower()  
    return any(path.endswith('/' + keyword.lower()) for keyword in keywords)

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return webdriver.Chrome(service=service, options=options)

def normalize_url(url):
    parsed = urlparse(url)
    normalized = parsed._replace(query="", fragment="").geturl()
    return normalized

def scrape_site(start_url, keywords):

    driver = setup_driver()
    visited = set()
    base_domain = urlparse(start_url).netloc
    to_visit = [start_url]

    all_content = ""

    while to_visit:
        current_url = to_visit.pop(0)
        normalized_url = normalize_url(current_url)
        if normalized_url in visited:
            continue
        visited.add(normalized_url)

        driver.get(current_url)
        driver.implicitly_wait(10) 

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.get_text(separator=' ', strip=True)
        title = driver.title if driver.title else 'No Title'

        all_content += f"## {title}\n\n{content}\n\n---\n\n"

        for link in soup.find_all('a', href=True):
            abs_link = urljoin(current_url, link['href'])
            if (is_valid_url(abs_link, base_domain) and abs_link not in visited and 
                ends_with_keywords(abs_link, keywords)):
                to_visit.append(abs_link)

    driver.quit()

    os.makedirs('Data', exist_ok=True)
    filename = sanitize_filename(base_domain) + '.md'
    with open(os.path.join('Data', filename), 'w', encoding='utf-8') as file:
        file.write(all_content)

keywords = [
    'connect', 'contact-us', 'get-in-touch', 'contact', 'global-presence',
    'about', 'about-us', 'who-we-are', 'our-story', 'company-info',
    'relationships', 'portfolio'
]


# scrape_site('https://www.accel.com', keywords)

scrape_site('https://www.a16z.com', keywords)

vc_websites = [
    'https://www.accel.com', 'https://www.a16z.com', 'https://www.greylock.com',
    'https://www.benchmark.com', 'https://www.sequoiacap.com', 'https://www.indexventures.com',
    'https://www.kpcb.com', 'https://www.lsvp.com', 'https://www.matrixpartners.com',
    'https://www.500.co', 'https://www.sparkcapital.com', 'https://www.insightpartners.com'
]



