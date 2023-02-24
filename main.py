import re
import time
# from socket import socket

import httpx
import requests
from selectolax.lexbor import SelectolaxError
from requests import ConnectTimeout
from selectolax.parser import HTMLParser
import fake_useragent
from random import choice
from dataclasses import dataclass, asdict
import csv
from os import path

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from requests_html import HTMLSession

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

# def http_version(url, ua, cookies_list, proxies):
#     cookies = dict()
#     for item in cookies_list:
#         cookies[item['name']] = item['value']
#     print(cookies)
#
#     header = {
#         'User-Agent': ua
#     }
#     print(header)
#
#     proxies = {
#         "all://": f"http://{choice(proxies)}"
#     }
#
#     print(proxies)
#
#     with httpx.Client(http2=True, cookies=cookies, headers=header, proxies=proxies) as client:
#         response = client.get(url)
#     print(response.http_version)

def webdriver_setup(proxy = None):
    ip, port = proxy.split(sep=':')
    ua = fake_useragent.UserAgent()
    while 1:
        useragent = ua.random
        if 'Windows' in useragent:
            print(useragent)
            break
        else:
            continue

    firefox_options = Options()
    firefox_options.add_argument('-headless')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.page_load_strategy = "eager"
    firefox_options.add_argument('-profile')
    firefox_options.add_argument(r'C:\Users\Haritz\AppData\Roaming\Mozilla\Firefox\Profiles\7w9b4myx.default-release')
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
    firefox_options.set_preference('dom.webdriver.enable', False)
    firefox_options.set_preference('useAutomationExtension', False)

    driver = webdriver.Firefox(options=firefox_options)
    return driver

def webdriver_setup2(proxy, useragent):
    ip, port = proxy.split(sep=':')

    firefox_options = Options()
    firefox_options.add_argument('-headless')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.page_load_strategy = "eager"
    firefox_options.add_argument('-profile')
    firefox_options.add_argument(r'C:\Users\Haritz\AppData\Roaming\Mozilla\Firefox\Profiles\7w9b4myx.default-release')
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
    firefox_options.set_preference('dom.webdriver.enable', False)
    firefox_options.set_preference('useAutomationExtension', False)

    driver = webdriver.Firefox(options=firefox_options)
    return driver

# def sw_setup(proxy):
#     ip, port = proxy.split(sep=':')
#     ua = fake_useragent.UserAgent()
#     useragent = ua.random
#     firefox_options = FirefoxOptions()
#     # firefox_options.add_argument('-headless')
#     firefox_options.add_argument('--no-sandbox')
#     # firefox_options.add_argument("-profile")
#     # firefox_options.add_argument(r'C:\Users\Haritz\AppData\Roaming\Mozilla\Firefox\Profiles\7w9b4myx.default-release')
#     firefox_options.page_load_strategy = "eager"
#     firefox_options.set_preference("general.useragent.override", useragent)
#     firefox_options.set_preference('network.proxy.type', 1)
#     firefox_options.set_preference('network.proxy.socks', ip)
#     firefox_options.set_preference('network.proxy.socks_port', int(port))
#     firefox_options.set_preference('network.proxy.socks_version', 4)
#     firefox_options.set_preference('network.proxy.socks_remote_dns', True)
#     firefox_options.set_preference('network.proxy.http', ip)
#     firefox_options.set_preference('network.proxy.http_port', int(port))
#     firefox_options.set_preference('network.proxy.ssl', ip)
#     firefox_options.set_preference('network.proxy.ssl_port', int(port))
#     firefox_options.set_preference("dom.webdriver.enabled", False)
#     firefox_options.set_preference('useAutomationExtension', False)

#     sw_opt = {
#     'proxy': {
#         "http://": f"http://{proxy}",
#         "https://": f"https://{proxy}"
#     }
# }
#     driver = Firefox(options=firefox_options)
#
#     return driver

def get_cookies(url, proxies):
    print("Getting cookies...")
    proxy = choice(proxies)
    driver = webdriver_setup(proxy)
    # driver.maximize_window()
    driver.fullscreen_window()
    driver.delete_all_cookies()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'nav[aria-label="pagination"]')))
    cookies = driver.get_cookies()
    for cookie in cookies:
        print(f"{cookie['name']}: {cookie['value']}")
    ua = driver.execute_script("return navigator.userAgent")
    driver.quit()
    return cookies, ua

# def get_headers(url, proxies):
#     print("Getting headers...")
#     proxy = choice(proxies)
#     print(proxy)
#     driver = sw_setup(proxy)
#     driver.maximize_window()
#     driver.delete_all_cookies()
#     driver.get(url)
#
#     wait = WebDriverWait(driver, 30)
#     wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'nav[aria-label="pagination"]')))
    # try:
    #     wait.until(ec.element_to_be_clickable((By.ID, 'ccmgt_explicit_accept'))).click()
    # except:
    #     print('no cookies')
    #     pass

    # request_list = driver.requests
    # del driver.requests
    # # driver.quit()
    # result = dict()
    # for i in request_list:
    #     print(i.headers)
    #     if i.headers['sec-fetch-dest'] == 'document' and i.headers.get('cookie') is not None:
    #        for item in i.headers:
    #            result[item] = i.headers[item]
    #        break
    #     else:
    #         continue
    # # value = input("SCRIPT ENDED\n")
    # return result

# def get_job_urls(url, ua, cookies_list, proxies):
#     print("Getting job urls...")
#     next_url = url
#     endofpage = False
#     cookies = dict()
#     for item in cookies_list:
#         cookies[item['name']] = item['value']
#
#     headers={
#         'user-agent': ua
#     }
#
#     job_urls = list()
#     while not endofpage:
#         proxies = {
#             "all://": f"http://{choice(proxies)}"
#         }
#         print(proxies)
#
#         with httpx.Client(cookies=cookies, headers=headers, proxies=proxies, timeout=(3,30)) as client:
#             response = client.get(url=next_url)
#         print(response.text)
#         job_tree = HTMLParser(response.text)
#         print(job_tree.css_first('title').text())
#         try:
#             parent_next_tree = job_tree.css_first('nav[aria-label="pagination"]')
#             next_url = parent_next_tree.css_first('a[aria-label="Nächste"]').attributes['href']
#             parent_job_tree = job_tree.css('article.resultlist-19kpq27')
#             for i in parent_job_tree:
#                 job_url = i.css_first('a.resultlist-w3sgr').attributes['href']
#                 job_urls.append(job_url)
#         except Exception as e:
#             print(e)
#             endofpage = True
#     return job_urls

def get_job_urls2(url, ua, cookies_list, proxies):
    print("Getting job urls...")
    next_url = url
    endofpage = False
    cookies = dict()
    for item in cookies_list:
        cookies[item['name']] = item['value']
    last_url = None
    job_urls = list()
    while not endofpage:
        if last_url == next_url:
            break
        else:
            try:
                selected_proxy = choice(proxies)
                formated_proxies = {
                    "http": f"http://{selected_proxy}",
                    "https": f"http://{selected_proxy}"
                }
                print(selected_proxy)

                headers = {
                    'user-agent': ua
                }

                client = HTMLSession()
                response = client.get(url=next_url, cookies=cookies, proxies=formated_proxies, timeout=(3,30), allow_redirects=True)
                response.html.render(sleep=5)
                try:
                    parent_next_tree = response.html.find('nav[aria-label="pagination"]', first=True)
                    last_url = next_url
                    next_url = parent_next_tree.find('a[aria-label="Nächste"]', first=True).attrs['href']
                    parent_job_tree = response.html.find('article.resultlist-19kpq27')
                    for i in parent_job_tree:
                        job_url = i.find('a.resultlist-w3sgr', first=True).attrs['href']
                        print(job_url)
                        job_urls.append(job_url)
                        print(f"{len(job_urls)} job url(s) are collected")
                except Exception as e:
                    print(e)
                    endofpage = True
            except ConnectTimeout:
                continue
    print('get jobs urls completed')
    return job_urls

def get_job_urls3(url, proxies):
    print("Getting job urls...")
    next_url = url
    last_url = None
    job_urls = list()
    ua = fake_useragent.UserAgent()
    while 1:
        useragent = ua.random
        if 'Windows' in useragent:
            print(useragent)
            break
        else:
            continue
    while 1:
        if last_url == next_url:
            break
        else:
            trials = 0
            while trials < 3:
                try:
                    proxy = choice(proxies)
                    driver = webdriver_setup2(proxy=proxy, useragent=useragent)
                    # driver.maximize_window()
                    driver.fullscreen_window()
                    driver.delete_all_cookies()
                    driver.get(next_url)
                    wait = WebDriverWait(driver, 10)
                    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'nav[aria-label="pagination"]')))
                    html = driver.page_source
                    driver.quit()
                    response = HTMLParser(html)
                    parent_next_tree = response.css_first('nav[aria-label="pagination"]')
                    last_url = next_url
                    next_url = parent_next_tree.css_first('a[aria-label="Nächste"]').attributes['href']
                    parent_job_tree = response.css('article.resultlist-19kpq27')
                    for i in parent_job_tree:
                        job_url = i.css_first('a.resultlist-w3sgr').attributes['href']
                        print(job_url)
                        job_urls.append(job_url)
                        print(f"{len(job_urls)} job url(s) are collected")
                except Exception as e:
                    print(e)
                    driver.quit()
                    ua = fake_useragent.UserAgent()
                    while 1:
                        useragent = ua.random
                        if 'Windows' in useragent:
                            print(useragent)
                            break
                        else:
                            continue
                    trials += 1
    print('get jobs urls completed')
    return job_urls

def get_website(search_term, proxy):
    print("Searching for company website...")
    formated_proxies = {
        "all://": f"http://{proxy}"
    }
    # print(proxy)

    ua = fake_useragent.UserAgent()
    while 1:
        useragent = ua.random
        if 'Windows' in useragent:
            # print(useragent)
            break
        else:
            continue
    header = {
        "user-agent": useragent
    }

    if search_term != None:
        url = f"https://html.duckduckgo.com/html/?q={re.sub('[^A-Za-z0-9]+', '+', search_term)}"
        with requests.Session() as client:
            response = client.get(url, headers=header, proxies=formated_proxies, timeout=(5, 27))
        tree = HTMLParser(response.text)
        result = tree.css_first("div.serp__results > div#links.results > div.result.results_links.results_links_deep.web-result > div.links_main.links_deep.result__body > div.result__extras > div.result__extras__url > a.result__url").text().strip()
    else:
        result = None
    return result

def get_linkedin(search_term, proxy):
    print("Searching for company linkedin...")
    formated_proxies = {
        "all://": f"http://{proxy}"
    }
    # print(proxy)

    ua = fake_useragent.UserAgent()
    while 1:
        useragent = ua.random
        if 'Windows' in useragent:
            # print(useragent)
            break
        else:
            continue
    header = {
        "user-agent": useragent
    }

    if search_term != None:
        url = f"https://html.duckduckgo.com/html/?q={re.sub('[^A-Za-z0-9]+', '+', search_term)}+linkedin"
        with requests.Session() as client:
            response = client.get(url, headers=header, proxies=formated_proxies, timeout=(5, 27))
        tree = HTMLParser(response.text)
        result = tree.css_first("div.serp__results > div#links.results > div.result.results_links.results_links_deep.web-result > div.links_main.links_deep.result__body > div.result__extras > div.result__extras__url > a.result__url").text().strip()
    else:
        result = None
    return result

def get_company_urls(job_url, proxies):
    print('Getting company url...')
    selected_proxy = choice(proxies)
    formated_proxies = {
        "http": f"http://{selected_proxy}",
        "https": f"http://{selected_proxy}"
    }
    print(selected_proxy)

    ua = fake_useragent.UserAgent()
    while 1:
        useragent = ua.random
        if 'Windows' in useragent:
            print(useragent)
            break
        else:
            continue
    header = {
        "user-agent": "insomnia/2022.7.5"
    }

    # with httpx.Client(headers=header, proxies=formated_proxies, timeout=(3,27), http2=True) as client:
    #     response = client.get(job_url)
    # print(response.text)
    client = HTMLSession()
    response = client.get(url=job_url, proxies=formated_proxies, timeout=(3, 30),
                          allow_redirects=True)
    response.html.render(sleep=5, timeout=100)
    datas = response.html.find('div[data-lang="de"]', first=True).text.split('\n')
    company_name = datas[0]
    print(company_name)
    for item in datas:
        if 'http://www' in item:
            company_website = item
            break
        else:
            company_website = None
            continue
    if company_website == None:
        proxy = choice(proxies)
        company_website = get_website(company_name, proxy)

    # try:
    #     company_website = response.html.find("a.StyledMetaDataLink-sc-ozf680.fcJvAT", first=True).attrs['href']
    # except SelectolaxError:
    #     proxy = choice(proxies)
    #     company_website = get_website(company_name, proxy)
    print(company_website)
    proxy = choice(proxies)
    company_linkedin = get_linkedin(company_name, proxy)
    print(company_linkedin)
    new_item = Company(name=company_name, website=company_website, linkedin=company_linkedin)
    print("=================================================================================")
    return asdict(new_item)

def main():
    proxies = ['192.126.250.22:8800',
               '192.126.253.48:8800',
               '192.126.253.197:8800',
               '192.126.253.134:8800',
               '192.126.253.59:8800',
               '192.126.250.223:8800']
    url = 'https://www.stepstone.de/jobs/account-executive?page=1&sort=2&action=sort_publish'

    # cookies, ua = get_cookies(url, proxies=proxies)
    # job_urls = get_job_urls2(url, ua=ua, cookies_list=cookies, proxies=proxies)
    job_urls = get_job_urls3(url, proxies=proxies)
    print(job_urls)
    for x in job_urls:
        company_urls = get_company_urls(x, proxies=proxies)
        to_csv(company_urls, 'Account Executive.csv')

if __name__ == '__main__':
    main()