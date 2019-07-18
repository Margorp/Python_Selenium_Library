import time, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CHROME_DRIVER_PATH = 'H:\Storage\Download\Temp\chromedriver_win32(75.0.3770.140)\chromedriver'

def get_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument('--proxy-bypass-list=*')
    return options

def get_executable_path():
    return CHROME_DRIVER_PATH

def download_html_by_chrome_driver(chrome_driver, url, validate_id=None, timeout_seconds=60):
    chrome_driver.get(url)
    if validate_id is not None:
        wait = WebDriverWait(chrome_driver, timeout_seconds)
        wait.until(EC.presence_of_element_located((By.ID, validate_id)))
    else:
        time.sleep(timeout_seconds)
    html = chrome_driver.page_source
    return html

def download_html_by_chrome(url, validate_id=None, timeout_seconds=60):
    chrome_driver = webdriver.Chrome(executable_path = get_executable_path(), options = get_options())
    html = download_html_by_chrome_driver(chrome_driver, url, validate_id, timeout_seconds)
    chrome_driver.quit()
    return html

def download_htmls_by_chrome(urls, validate_id=None, timeout_seconds = 60):
    htmls = []
    chrome_driver = webdriver.Chrome(executable_path = get_executable_path(), options = get_options())    
    for url in urls:
        html = download_html_by_chrome_driver(chrome_driver, url, validate_id, timeout_seconds)
        htmls.append(html)
    chrome_driver.quit()
    return htmls

def test_chrome_module():
    # prepare test urls
    tmp_url = 'https://racing.hkjc.com/racing/information/chinese/Racing/LocalResults.aspx?RaceDate=1979/09/22&Racecourse=HV&RaceNo=%d'
    urls = []
    for i in range(1,10):
        url = tmp_url % i
        urls.append(url)

    # download all htmls
    start_time = datetime.datetime.now()
    htmls = download_htmls_by_chrome(urls, 'mainContainer')
    end_time = datetime.datetime.now()
    print('elapsed time:', end_time - start_time)
    
    # check results
    for i, html in enumerate(htmls):
        check = len(html)>100000
        print(i+1, len(html), 'passed' if check else 'failed')
