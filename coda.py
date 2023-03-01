# write your code
import re
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

driver.get('https://coda.io/@kenny/coda-alumni-list')
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'columnHeaderRoot')))

elements = driver.find_elements(by="class name", value="columnHeaderRoot")
for element in elements:
    if element.text.strip() != "":
        print(element.text.strip())
# print(element.text)

def execute_script(url):
    columns = []
    rows = []

    # TODO: need to determine if it is the right page to scrape such as https://coda.io/@opendoorosn/opendoor-os-national-talent-board

    filename = 'Coda-' + re.search(r'([^\/]+)$', url).group(0)
    path = Path(filename)
    if not path.is_file():
        print('File not found: Downloading the file')
        response = get(url)
        file = open(filename,'w', encoding="utf-8")
        file.write(response.text)
        file.close()


    file = open(filename,'r', encoding="utf-8");
    html_soup = BeautifulSoup(file.read(), 'html.parser')
    columns_headers = html_soup.find_all('div', class_ = 'columnHeaderRoot')
    num_columns_headers = len(columns_headers)
    i = 0
    print(len(columns_headers))
    for container in columns_headers:
        target = container.find('div', class_ = 'kr-text-input-view-measurement')
        columns.append(target.text)
        print(target.text)
        i+=1
        if i == num_columns_headers / 2:
            break

    # check if the page contain vertical group, that means there are merged cells that need to handle
    vertical_groups = html_soup.select('div[data-coda-ui-id*="pivotVerticalGroup"]')
    print(len(vertical_groups))


    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(filename+'.csv')

# execute_script('https://coda.io/@alumni/zoom-alumni-list')
# execute_script('https://coda.io/@kenny/coda-alumni-list')