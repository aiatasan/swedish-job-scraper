# job_info_scraper.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import time

def scrape_job_posting(url):
    """
    Fetches the job posting from the given URL and extracts the required fields,
    including separating the job description into sections.
    """
    # Fetch the HTML content
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')

    def get_job_id(soup):
        # Try to extract from JSON data in script tag with id="__NEXT_DATA__"
        script_tag = soup.find('script', id='__NEXT_DATA__')
        if script_tag:
            try:
                json_data = json.loads(script_tag.string)
                job_data = json_data['props']['pageProps']['initialApolloState']
                for key in job_data:
                    if key.startswith('MonolithJob'):
                        job_id = job_data[key].get('listId')
                        return job_id
            except (json.JSONDecodeError, KeyError):
                pass
        # Alternatively, extract from URL
        url_parts = url.strip('/').split('/')
        job_id = url_parts[-1] if url_parts else None
        return job_id

    def parse_swedish_date(date_str):
        months = {
            'januari': '01',
            'februari': '02',
            'mars': '03',
            'april': '04',
            'maj': '05',
            'juni': '06',
            'juli': '07',
            'augusti': '08',
            'september': '09',
            'oktober': '10',
            'november': '11',
            'december': '12'
        }
        for swedish_month, month_number in months.items():
            if swedish_month in date_str.lower():
                date_str = date_str.lower().replace(swedish_month, month_number)
                break
        try:
            return datetime.strptime(date_str.strip(), '%d %m %Y').date()
        except ValueError:
            return None

    # Extract the fields
    job_id = get_job_id(soup)

    job_title_tag = soup.find('h1', attrs={'data-cy': 'subject'})
    job_title = job_title_tag.get_text(strip=True) if job_title_tag else None

    company_tag = soup.find('a', attrs={'aria-label': re.compile(r'^Fler jobb från')})
    company = company_tag.get_text(strip=True) if company_tag else None

    # Replace 'text' with 'string' in find() calls
    location_label = soup.find('div', string='Område')
    location = location_label.find_next_sibling('div').get_text(strip=True) if location_label else None

    employment_type_label = soup.find('div', string='Typ av anställning')
    employment_type_div = employment_type_label.find_next_sibling('div') if employment_type_label else None
    employment_type = employment_type_div.get_text(separator=', ', strip=True) if employment_type_div else None

    deadline_label = soup.find('div', string='Sista ansökningsdag')
    deadline_div = deadline_label.find_next_sibling('div') if deadline_label else None
    application_deadline_text = deadline_div.get_text(strip=True) if deadline_div else None
    application_deadline = parse_swedish_date(application_deadline_text.split('(')[0].strip()) if application_deadline_text else None

    apply_button = soup.find('a', {'data-cy': 'apply-button'})
    application_link = apply_button['href'] if apply_button else None

    # Job Description: Extract and split into sections
    description_div = soup.find('div', class_=re.compile(r'^sc-.*flrgoh$'))
    job_description_sections = {}
    if description_div:
        description_text = description_div.get_text(separator='\n', strip=True)
        # Split the text into sections based on headings
        sections = re.split(r'\n(?=[A-ZÅÄÖ &]+(?:\n|$))', description_text)
        current_section = None
        for part in sections:
            lines = part.strip().split('\n')
            if lines:
                # Check if the first line is a heading
                heading = lines[0].strip()
                content = '\n'.join(lines[1:]).strip()
                if re.match(r'^[A-ZÅÄÖ &]+$', heading):
                    current_section = heading
                    job_description_sections[current_section] = content
                else:
                    # If not a heading, append to previous content
                    if current_section:
                        job_description_sections[current_section] += '\n' + part.strip()
                    else:
                        # If no current section, create a default section
                        current_section = 'Description'
                        job_description_sections[current_section] = part.strip()
    else:
        job_description_sections = None

    # Company Description
    company_description_div = soup.find('div', class_=re.compile(r'^sc-5fe98a8b-19'))
    company_description = company_description_div.get_text(separator='\n', strip=True) if company_description_div else None

    date_posted_label = soup.find('div', string='Publiceringsdatum')
    date_posted_div = date_posted_label.find_next_sibling('div') if date_posted_label else None
    date_posted_text = date_posted_div.get_text(strip=True) if date_posted_div else None
    date_posted = parse_swedish_date(date_posted_text) if date_posted_text else None

    # Prepare the data dictionary
    data = {
        'id': job_id,
        'job_title': job_title,
        'company': company,
        'location': location,
        'employment_type': employment_type,
        'application_deadline': application_deadline,
        'application_link': application_link,
        'job_description_sections': job_description_sections,
        'company_description': company_description,
        'date_posted': date_posted
    }

    return data

if __name__ == "__main__":
    for i in range(2196925, 2197401):
        url = f"https://jobb.blocket.se/ledigt-jobb/{i}"
        try:
            job_data = scrape_job_posting(url)
            if job_data:
                # Process the job_data 
                print(f"Scraped job ID {job_data['id']}: {job_data['job_title']}")
            else:
                print(f"No data found for job ID {i}")
        except Exception as err:
            print(f"An error occurred for job ID {i}: {err}")
        
        time.sleep(1)  # Sleep for 1 second
