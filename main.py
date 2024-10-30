from scrapping import get_jobs_list
from job_info_scrapper import scrape_job_posting
import pandas as pd


url = "https://jobb.blocket.se/lediga-jobb"


jobs_list = get_jobs_list(url)
counter = 0
folder = "data"
excel_list = []

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

for job_posting_url in jobs_list:
    job_posting = scrape_job_posting(job_posting_url)
    counter += 1
    excel_list.append(job_posting)
    if counter % 999 == 0:
        file_name = f"{folder}{counter}.xlsx"
        save_to_excel(excel_list, file_name)
        excel_list = []

file_name = f"{folder}{counter}.xlsx"
save_to_excel(excel_list, file_name)