from data_preparation.scraping import scrape_employee_gsheet
from data_preparation.scraping import scrape_employee_coda

def download_employee_csv(list_name, url, output_dir):
    url_parts = url.split('/')
    if url_parts[2] == 'docs.google.com':
        return scrape_employee_gsheet.download_gsheet_csv(list_name, url, output_dir)
    elif url_parts[2] == 'coda.io':
        return scrape_employee_coda.download_coda_csv(list_name, url, output_dir)
    else:
        return None
