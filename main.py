import httpx
import requests
from selectolax.parser import HTMLParser

def get_job_urls(url):
    next_url = url
    endofpage = False
    while not endofpage:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }

        with httpx.Client() as client:
            response = client.get(url=next_url, headers=header)
        job_tree = HTMLParser(response.text)
        print(job_tree.css_first('title').text())
        job_urls = list()
        try:
            parent_next_tree = job_tree.css_first('nav[aria-label="pagination"]')
            next_url = parent_next_tree.css_first('a[aria-label="Nächste"]').attributes['href']
            parent_job_tree = job_tree.css('article.resultlist-19kpq27')
            for i in parent_job_tree:
                job_url = i.css_first('a.resultlist-w3sgr').attributes['href']
                job_urls.append(job_url)
        except Exception as e:
            print(e)
            endofpage = True
    return job_urls

def main():
    url = 'https://www.stepstone.de/jobs/junior-sales/in-berlin?radius=30&sort=2&action=sort_publish'
    job_urls = get_job_urls(url)
    print(job_urls)

if __name__ == '__main__':
    main()