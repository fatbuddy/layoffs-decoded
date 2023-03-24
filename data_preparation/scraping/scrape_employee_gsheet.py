import pandas as pd
import requests
from urllib.parse import urlparse, urlunparse
import csv
import re
from parsel import Selector

USER_AGENT_HEADER={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0"}

def download_gsheet_csv(list_name, url, output_dir):
    print("---------------------\n")
    print(f"{list_name}")
    err = None
    parsed_url = urlparse(url)
    url_parts = parsed_url.path.split('/')
    if parsed_url.netloc != 'docs.google.com':
        print("not a google sheet")
        return None

    original_link_status = requests.get(url, headers=USER_AGENT_HEADER).status_code
    if original_link_status != 200:
        print(f"original url: {original_link_status}")
        return None

    if 'e' in url_parts:
        print("export url, manual scraping needed")
        return scrape_gsheet_manual(list_name, url, output_dir, isExportUrl=True)

    if gsheet_has_multiple_sheets(url=url, isExportUrl=False):
        print("csv has multiple sheets, manual scraping needed")
        return scrape_gsheet_manual(list_name, url, output_dir, isExportUrl=False)

    if url_parts[2] == 'u' and url_parts[4] == 'd':
        url_parts = url_parts[:2] + url_parts[4:]

    query_string = f"format=csv&id={url_parts[3]}"
    if parsed_url.fragment != "":
        query_string = f"{query_string}&{parsed_url.fragment}"
    modified_path = '/'.join(url_parts[:4] + ["export"])
    modified_parsed_url = parsed_url._replace(
        path=modified_path,
        query=query_string,
        fragment="")
    csv_url = urlunparse(modified_parsed_url)
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
    return [f'{output_dir}/{list_name}.csv']

def scrape_gsheet_manual(list_name, url, output_dir, isExportUrl=False):
    directory_tabs = {
        "delivery hero": "Talent Directory",
        "doordash": "All Functions"
    }
    use_directory_tab = None
    for k, v in directory_tabs.items():
        if list_name.lower().find(k) > -1:
            use_directory_tab = v
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
    sheets = root.xpath('//table[contains(@class,"waffle")]')
    print(f"sheet count = {len(sheets)}")
    sheet_buttons = root.xpath('//li[contains(@id,"sheet-button")]')
    sheet_names = list([sb.xpath('descendant-or-self::*/text()').get() for sb in sheet_buttons])
    output_paths = []
    regex = re.compile(r".*(hire|hiring|recruit|job|company|resource|slack).*", re.IGNORECASE)
    for sheet_idx, sheet in enumerate(sheets):
        sheet_name = sheet_names[sheet_idx] if sheet_idx < len(sheet_names) else str(sheet_idx)
        print(sheet_name)
        if regex.match(sheet_name):
            print(f"skipping: sheet name {sheet_name}")
            continue
        if use_directory_tab is not None and sheet_name != use_directory_tab:
            print(f"skipping: sheet name {sheet_name} for {list_name}")
            continue
        html_rows = sheet.xpath('tbody/tr')
        print(len(html_rows))
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
        output_path = f'{output_dir}/{list_name}_{"".join(c for c in sheet_name if c.isalnum())}.csv'
        with open(output_path, 'w') as f:
            writer = csv.writer(f)
            for d in data:
                writer.writerow(d)
        output_paths.append(output_path)
    if len(output_paths) == 0:
        return None
    return output_paths

def gsheet_html_view(url, isExportUrl=False):
    html_url = url
    if not isExportUrl:
        url_parts = url.split('/')
        html_url = '/'.join(url_parts[:6] + ['htmlview'])
    return html_url

def gsheet_has_multiple_sheets(url, isExportUrl=False):
    html_url = gsheet_html_view(url, isExportUrl)
    resp = requests.get(html_url, headers=USER_AGENT_HEADER)
    if resp.status_code != 200:
        print(f'html url: {resp.status_code}')
        return False
    root = Selector(text=resp.text)
    sheets = root.xpath('//table[contains(@class,"waffle")]')
    return len(sheets) > 1

# layoff_list = pd.read_csv('layoff_fyi.csv', header=0, index_col=0)
# for row in layoff_list.iterrows():
#     list_name = row[1]['List Name']
#     sheet_url = row[1]['Link']
#     download_gsheet_csv(list_name, sheet_url)
