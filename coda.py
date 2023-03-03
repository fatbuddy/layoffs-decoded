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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
def execute_script(url):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get(url)
    
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'columnHeaderRoot')))
    html = driver.find_element(By.TAG_NAME, 'html')


    # times_scroll_down = 30
    # i=0
    # while i< times_scroll_down:
    #     driver.execute_script('document.querySelector(\'div[data-scroll-id="canvasScrollContainer"]\').scrollTo(0, '+str(i*500)+')')
    #     time.sleep(0.5)
    #     i+=1
    
    # time.sleep(10)
    file = open('test','w', encoding="utf-8")
    file.write(driver.page_source)
    file.close()


    # columns = []
    # rows = []
    # elements = driver.find_elements(by="class name", value="columnHeaderRoot")
    # for element in elements:
    #     if element.text.strip() != "":
    #         columns.append(element.text.strip())

    # vertical_groups = driver.find_elements(by="css selector", value='div[data-coda-ui-id*="pivotVerticalGroup"]')

    # if len(vertical_groups) > 0:
    #     for vertical_group in vertical_groups:
    #         column_header = vertical_group.find_element(by="css selector", value='div[role="columnheader"]').text
    #         cells = vertical_group.find_elements(by="css selector", value='div[data-reference-type="cell"]')
    #         entry = [column_header]
    #         for cell in cells:
    #             try:
    #                 anchor = cell.find_element(by="tag name", value="a")        
    #                 link = anchor.get_attribute('href')
    #                 print('link: '+link.replace("mailto:", ""))
    #                 entry.append(link.replace("mailto:", ""))
    #             except:
    #                 if not cell:
    #                     continue
    #                 if cell.text != "":
    #                     # determine if the field contains more than one value
    #                     labels = cell.find_elements(by="css selector", value='div[data-is-transparent-container="true"] > span')
    #                     if len(labels) > 1:
    #                         label_container = []
    #                         for label in labels:
    #                             label_container.append(label.text)
    #                         entry.append(label_container)
    #                         print(label_container)
    #                     else:
    #                         entry.append(cell.text)
    #         rows.append(entry)
            
    #     df = pd.DataFrame(rows, columns=columns)
    #     df.to_csv('test.csv')

    columns = []
    rows = []

    # TODO: need to determine if it is the right page to scrape such as https://coda.io/@opendoorosn/opendoor-os-national-talent-board

    # filename = 'Coda-' + re.search(r'([^\/]+)$', url).group(0)
    # path = Path(filename)
    # if not path.is_file():
    #     print('File not found: Downloading the file')
    #     response = get(url)
    #     file = open(filename,'w', encoding="utf-8")
    #     file.write(response.text)
    #     file.close()

    filename = 'test'
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
    if len(vertical_groups) > 0:
        for vertical_group in vertical_groups:
            column_header = vertical_group.select('div[role="columnheader"] .kr-cell')[0].text
            rows = process_row(rows, vertical_group, column_header=column_header)
    else:
        # this is for the case which does not contain vertical group such as https://coda.io/@daanyal-kamaal/goto-alumni-list
        rows = process_row(rows, html_soup)            



    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(filename+'.csv')

def process_row(rows, parent, column_header = None):
    row_containers = parent.select('div[data-reference-type="row"]')
    print("total rows: "+str(len(row_containers)))
    for row_container in row_containers:
        cells = row_container.select('div[data-reference-type="cell"]')
        if column_header is not None:
            entry = [column_header]
        else:
            entry = []
        for cell in cells:
            anchor = cell.find("a")        
            if anchor:
                link = anchor.get('href')
                entry.append(link.replace("mailto:", ""))
            else:
                if not cell:
                    continue
                # if cell.text != "":
                # determine if the field contains more than one value
                labels = cell.select('div[data-is-transparent-container="true"] > span')
                if len(labels) > 1:
                    label_container = []
                    for label in labels:
                        label_container.append(label.text)
                    entry.append(label_container)
                    # print(label_container)
                else:
                    entry.append(cell.text)
        print(entry)
        print('----------------')
        rows.append(entry)
    return rows

# first case: base cases
# execute_script('https://coda.io/@daanyal-kamaal/goto-alumni-list')

# second case: merged cells on the 1st column
# execute_script('https://coda.io/@alumni/zoom-alumni-list')

# third case: javascript driven loading the data
# execute_script('https://coda.io/@kenny/coda-alumni-list')


# cases not working yet
# the rows change when scrolling
# also have addition links for scraping
execute_script('https://coda.io/d/Talent-Board_dN7cqX2rCM4/Candidates_suM29#_luRyI')

