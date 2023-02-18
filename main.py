import time

import httpx
import requests_html
from selectolax.parser import HTMLParser
import fake_useragent
from random import choice
from dataclasses import dataclass
import csv
from os import path

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from seleniumwire.webdriver import Firefox, FirefoxOptions

@dataclass
class Company:
    name: str
    website: str
    linkedin: str

def to_csv(data, filename):
    file_exists = path.isfile(filename)

    with open(filename, 'a', encoding='utf-16') as f:
        headers = ['name', 'website', 'linkedin']
        writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def http_version(url, ua, cookies_list, proxies):
    cookies = dict()
    for item in cookies_list:
        cookies[item['name']] = item['value']
    print(cookies)

    header = {
        'User-Agent': ua
    }
    print(header)

    proxies = {
        "all://": f"http://{choice(proxies)}"
    }

    print(proxies)

    with httpx.Client(http2=True, cookies=cookies, headers=header, proxies=proxies) as client:
        response = client.get(url)
    print(response.http_version)

def webdriver_setup(proxy = None):
    ip, port = proxy.split(sep=':')
    ua = fake_useragent.UserAgent()
    useragent = ua.firefox
    firefox_options = Options()

    # firefox_options.add_argument('-headless')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.page_load_strategy = "eager"

    firefox_options.set_preference("general.useragent.override", useragent)
    firefox_options.set_preference('network.proxy.type', 1)
    firefox_options.set_preference('network.proxy.socks', ip)
    firefox_options.set_preference('network.proxy.socks_port', int(port))
    firefox_options.set_preference('network.proxy.socks_version', 4)
    firefox_options.set_preference('network.proxy.socks_remote_dns', True)
    firefox_options.set_preference('network.proxy.http', ip)
    firefox_options.set_preference('network.proxy.http_port', int(port))
    firefox_options.set_preference('network.proxy.ssl', ip)
    firefox_options.set_preference('network.proxy.ssl_port', int(port))

    driver = webdriver.Firefox(options=firefox_options)
    return driver

def sw_setup(proxy):
    ip, port = proxy.split(sep=':')
    ua = fake_useragent.UserAgent()
    useragent = ua.random
    firefox_options = FirefoxOptions()

    # firefox_options.add_argument('-headless')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.page_load_strategy = "eager"
    firefox_options.set_preference("general.useragent.override", useragent)
    firefox_options.set_preference('network.proxy.type', 1)
    firefox_options.set_preference('network.proxy.socks', ip)
    firefox_options.set_preference('network.proxy.socks_port', int(port))
    firefox_options.set_preference('network.proxy.socks_version', 4)
    firefox_options.set_preference('network.proxy.socks_remote_dns', True)
    firefox_options.set_preference('network.proxy.http', ip)
    firefox_options.set_preference('network.proxy.http_port', int(port))
    firefox_options.set_preference('network.proxy.ssl', ip)
    firefox_options.set_preference('network.proxy.ssl_port', int(port))
    firefox_options.set_preference("dom.webdriver.enabled", False)
    firefox_options.set_preference('useAutomationExtension', False)

#     sw_opt = {
#     'proxy': {
#         "http://": f"http://{proxy}",
#         "https://": f"https://{proxy}"
#     }
# }
    driver = Firefox(options=firefox_options)

    return driver

def get_cookies(url, proxies):
    print("Getting cookies...")
    proxy = choice(proxies)
    driver = webdriver_setup(proxy)
    driver.delete_all_cookies()
    driver.get(url)
    wait = WebDriverWait(driver, 30)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input[data-at="searchbar-keyword-input"]')))
    cookies = driver.get_cookies()
    ua = driver.execute_script("return navigator.userAgent")
    driver.quit()
    return cookies, ua

def get_headers(url, proxies):
    print("Getting headers...")
    proxy = choice(proxies)
    print(proxy)
    driver = sw_setup(proxy)
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    try:
        wait.until(ec.element_to_be_clickable((By.ID, 'ccmgt_explicit_accept'))).click()
    except:
        pass

    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'nav[aria-label="pagination"]')))
    request_list = driver.requests
    del driver.requests
    driver.quit()
    result = dict()
    for i in request_list:
        # print(i.headers)
        if i.headers['sec-fetch-dest'] == 'document':
           for item in i.headers:
               result[item] = i.headers[item]
           break
        else:
            continue
    # value = input("SCRIPT ENDED\n")
    return result

def get_job_urls(url, headers, proxies):
    print("Getting job urls...")
    next_url = url
    endofpage = False
    while not endofpage:
        proxies = {
            "all://": f"http://{choice(proxies)}"
        }
        print(proxies)

        with httpx.Client(headers=headers, proxies=proxies, http2=True, follow_redirects=False) as client:
            response = client.get(url=next_url)
            print(response.history)
        print(response.text)
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

def get_job_urls2(url, headers, proxies):
    print("Getting job urls...")
    next_url = url
    endofpage = False
    while not endofpage:
        proxies = {
            "all://": f"http://{choice(proxies)}"
        }
        print(proxies)

        with requests_html.HTMLSession(headers=headers, proxies=proxies, http2=True, follow_redirects=False) as client:
            client.get(url=next_url)
            client.html.render()

        print(response.text)
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
    proxies = ['192.126.250.22:8800',
               '192.126.253.48:8800',
               '192.126.253.197:8800',
               '192.126.253.134:8800',
               '192.126.253.59:8800',
               '192.126.250.223:8800']
    url = 'https://www.stepstone.de/jobs/junior-sales?sort=2&action=sort_publish'
    header = get_headers(url, proxies=proxies)
    job_urls = get_job_urls(url, headers=header, proxies=proxies)
    print(job_urls)

if __name__ == '__main__':
    main()