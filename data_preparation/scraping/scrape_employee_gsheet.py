import pandas as pd
import requests
import csv
from parsel import Selector

USER_AGENT_HEADER={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0"}

def download_gsheet_csv(list_name, url, output_dir):
    print("---------------------\n")
    print(f"{list_name}")
    err = None
    url_parts = url.split('/')
    if url_parts[2] != 'docs.google.com':
        print("not a google sheet")
        return None
    if 'e' in url_parts:
        print("export url, manual scraping needed")
        return scrape_gsheet_manual(list_name, url, output_dir, isExportUrl=True)
    original_link_status = requests.get(url, headers=USER_AGENT_HEADER).status_code
    if original_link_status != 200:
        print(f"original url: {original_link_status}")
        return None
    if url_parts[4] == 'u' and url_parts[6] == 'd':
        url_parts = url_parts[:4] + url_parts[6:]
        
    csv_url = '/'.join(url_parts[:6] + [f'export?format=csv&id={url_parts[5]}'])
    resp = requests.get(csv_url, headers=USER_AGENT_HEADER)
    if resp.status_code != 200:
        print(f"csv url: {resp.status_code}, manual scraping needed")
        return scrape_gsheet_manual(list_name, url, output_dir, isExportUrl=False)
    with open(f'{output_dir}/{list_name}.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        reader = csv.reader(resp.content.decode('utf-8').splitlines())
        count = 0
        for row in reader:
            writer.writerow(row)
            count+=1
        print(count)
    return f'{output_dir}/{list_name}.csv'

def scrape_gsheet_manual(list_name, url, output_dir, isExportUrl=False):
    html_url = url
    if not isExportUrl:
        url_parts = url.split('/')
        html_url = '/'.join(url_parts[:6] + ['htmlview'])
#     print(html_url)
    resp = requests.get(html_url, headers=USER_AGENT_HEADER)
    if resp.status_code != 200:
        print(f'html url: {resp.status_code}')
        return None
    root = Selector(text=resp.text)
    html_rows = root.xpath('//table[contains(@class,"waffle")]/tbody/tr')
#     print(len(html_rows))
    data = []
    for row in html_rows:
        tds = []
        for td in row.xpath('td'):
            td_text = td.xpath('descendant-or-self::*/text()').get()
            if td_text:
                tds.append(td_text)
            else:
                tds.append("")
        if len([s for s in tds if s]):
            data.append(tds)
    print(len(data))
    with open(f'{output_dir}/{list_name}.csv', 'w') as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow(d)
    return f'{output_dir}/{list_name}.csv'

# layoff_list = pd.read_csv('layoff_fyi.csv', header=0, index_col=0)
# for row in layoff_list.iterrows():
#     list_name = row[1]['List Name']
#     sheet_url = row[1]['Link']
#     download_gsheet_csv(list_name, sheet_url)
