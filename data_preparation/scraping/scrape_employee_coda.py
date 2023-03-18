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
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse, urlunparse
import traceback
import time

def execute_script(url, filename='test'):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    columns = []
    rows = []
    
    times_scroll_down = 50
    unvisited_link = [url]
    page_visit = []
    parsed_url = urlparse(url)
    current_page = parsed_url.path
    while len(unvisited_link) > 0:
        url = unvisited_link.pop()
        print("Current URL: " + url)
        page_visit.append(url)
        driver.get(url)
        wait = WebDriverWait(driver, 60)
        try:
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'columnHeaderRoot')))
            scroll_time=0
            previous_result = []
            while scroll_time < times_scroll_down:
                driver.execute_script('document.querySelector(\'div[data-scroll-id="canvasScrollContainer"]\').scrollTo(0, '+str(scroll_time*1000)+')')
                scroll_time += 1
                time.sleep(5)
                # file = open('test','w', encoding="utf-8")
                # file.write()
                # file.close()
                
                # file = open(filename,'r', encoding="utf-8");
                html_code = driver.page_source
                html_soup = BeautifulSoup(html_code, 'html.parser')
                columns_headers = html_soup.find_all('div', class_ = 'columnHeaderRoot')
                num_columns_headers = len(columns_headers)
                i = 0
                if len(columns) == 0:
                    for container in columns_headers:
                        target = container.find('div', class_ = 'kr-text-input-view-measurement')
                        columns.append(target.text)
                        print(target.text)
                        i+=1
                        if i == num_columns_headers / 2:
                            break

                # check if the page contain vertical group, that means there are merged cells that need to handle
                vertical_groups = html_soup.select('div[data-coda-ui-id*="pivotVerticalGroup"]')
                # for fixing kenny/coda-alumni-list 
                if len(vertical_groups) == 0:
                    vertical_groups = html_soup.select('div[data-reference-type*="vertical-group-headers"] > div')
                if len(vertical_groups) > 0:
                    last_appended_row = []
                    for vertical_group in vertical_groups:
                        if len(vertical_group.select('div[role="columnheader"] .kr-cell')) > 0:
                            column_header = vertical_group.select('div[role="columnheader"] .kr-cell')[0].text
                            print("Column header: "+column_header)
                            rows, appended_row = process_row(rows, vertical_group, column_header=column_header)
                            last_appended_row += appended_row
                    if previous_result == last_appended_row:
                        break
                    previous_result = last_appended_row
                else:
                    # this is for the case which does not contain vertical group such as https://coda.io/@daanyal-kamaal/goto-alumni-list 
                    rows, appended_row = process_row(rows, html_soup)            
                    if previous_result == appended_row:
                        break
                    previous_result = appended_row
        except TimeoutException as t_e:
            print("Element not found! Looks for the link!")
            html_soup = BeautifulSoup(driver.page_source, 'html.parser')
            anchors = html_soup.find_all("a", href=True)
            for anchor in anchors:
                href = anchor.get('href')
                if href == current_page:
                    continue
                if href in page_visit:
                    continue
                if current_page in href:
                    target_page = urlunparse(parsed_url._replace(path=href))
                    unvisited_link.append(target_page)
            print(unvisited_link)
        except Exception:
            traceback.print_exc()
    driver.quit()
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(filename+'.csv')

def process_row(rows, parent, column_header = None):
    row_containers = parent.select('div[data-reference-type="row"]')
    if column_header is not None:
        print("for header : "+column_header)
    print("total rows: "+str(len(row_containers)))
    appended_rows = []
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
        # print(entry)
        # print('----------------')
        if entry not in rows:
            rows.append(entry)
            appended_rows.append(entry)
    return rows, appended_rows

def download_coda_csv(list_name, url, output_dir):
    url_parts = url.split('/')
    if url_parts[2] != 'coda.io':
        print("not a coda sheet")
        return None
    # if (url == 'https://coda.io/d/Talent-Board_dN7cqX2rCM4/Candidates_suM29#_luRyI' or 
    #     url == 'https://coda.io/@alumni/zoom-alumni-list'):
    #     print("skipping zoom-alumni-list/Talent-Board")
    #     return None
    execute_script(url, filename=f"{output_dir}/{list_name}")
    return f"{output_dir}/{list_name}.csv"
    

# first case: base cases
# execute_script('https://coda.io/@daanyal-kamaal/goto-alumni-list')

# second case: merged cells on the 1st column
# execute_script('https://coda.io/@alumni/zoom-alumni-list')

# third case: javascript driven loading the data
# execute_script('https://coda.io/@kenny/coda-alumni-list')

# forth case: additional link
# execute_script('https://coda.io/@opendoorosn/opendoor-os-national-talent-board')  

# cases not working yet
# the rows change when scrolling
# also have addition links for scraping
execute_script('https://coda.io/d/Talent-Board_dN7cqX2rCM4/Candidates_suM29#_luRyI')
