import requests
from bs4 import BeautifulSoup

def get_number_of_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    page_links = soup.find_all('a', attrs={"rel":"nofollow"})
    number_of_pages = [int(link.get_text()) for link in page_links if link.get_text().isdigit()]

    return max(number_of_pages)

def get_page_data(url, jobs_list):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    job_cards = soup.find_all('div', class_="sc-b071b343-0 eujsyo")
    for item in job_cards:
        href = "https://jobb.blocket.se" + item.a.attrs['href']
        jobs_list.append({"URL": href})

    return jobs_list

def get_next_url(base_url, page):
    return f"{base_url}?page={page}"

def get_jobs_list(url):
    jobs_list = []
    number_of_pages = get_number_of_pages(url)
    for page in range(1, int(number_of_pages) + 1):
            jobs_list = get_page_data(url, jobs_list)
            print(jobs_list)
            try:
                url = get_next_url("https://jobb.blocket.se/lediga-jobb", page + 1)
            except:
                break
            
    return jobs_list


get_jobs_list("https://jobb.blocket.se/lediga-jobb")
