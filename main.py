import re
import time
# from socket import socket

import httpx
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

    job_urls = list()
    while not endofpage:
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
        with httpx.Client(headers=header, proxies=formated_proxies, timeout=(3, 27)) as client:
            response = client.get(url)
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
        with httpx.Client(headers=header, proxies=formated_proxies, timeout=(3, 27)) as client:
            response = client.get(url)
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
    url = 'https://www.stepstone.de/jobs/junior-sales?page=1&sort=2&action=sort_publish'

    cookies, ua = get_cookies(url, proxies=proxies)
    job_urls = get_job_urls2(url, ua=ua, cookies_list=cookies, proxies=proxies)
    # job_urls = ['https://www.stepstone.de/cmp/de/w%c3%bcrth-elektronik-eisos-gmbh-%26-co-kg-75178/jobs',
    #                 'https://www.stepstone.de/cmp/de/osma-aufz%c3%bcge-albert-schenk-gmbh-%26-co-kg-53020/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/concat-ag-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/cosdamed-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/etengo-ag-69561/jobs',
    #                 'https://www.stepstone.de/cmp/de/grenke-ag-29945/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/osma-aufz%c3%bcge-albert-schenk-gmbh-%26-co-kg-53020/jobs',
    #                 'https://www.stepstone.de/cmp/de/osma-aufz%c3%bcge-albert-schenk-gmbh-%26-co-kg-53020/jobs',
    #                 'https://www.stepstone.de/cmp/de/jungheinrich-service-%26-parts-ag-%26-co-kg-246765/jobs',
    #                 'https://www.stepstone.de/cmp/de/oschatz-visuelle-medien-gmbh-%26-co-kg-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/tk-aufz%c3%bcge-gmbh-19937/jobs',
    #                 'https://www.stepstone.de/cmp/de/beta-systems-software-ag-1351/jobs',
    #                 'https://www.stepstone.de/cmp/de/consortium-gastronomie-gmbh-210278/jobs',
    #                 'https://www.stepstone.de/cmp/de/krongaard-gmbh-77857/jobs',
    #                 'https://www.stepstone.de/cmp/de/aristo-group-143539/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/mediaprint-infoverlag-gmbh-126743/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/igus%c2%ae-gmbh-4294/jobs',
    #                 'https://www.stepstone.de/cmp/de/mediaprint-infoverlag-gmbh-126743/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/krongaard-gmbh-77857/jobs',
    #                 'https://www.stepstone.de/cmp/de/rhenus-freight-logistics-gmbh-%26-co-kg-199327/jobs',
    #                 'https://www.stepstone.de/cmp/de/igus%c2%ae-gmbh-4294/jobs',
    #                 'https://www.stepstone.de/cmp/de/igus%c2%ae-gmbh-4294/jobs',
    #                 'https://www.stepstone.de/cmp/de/exklusive-klausur-und-tagungsst%c3%a4tten-gmbh-la-villa-am-starnberger-see-258280/jobs',
    #                 'https://www.stepstone.de/cmp/de/igus%c2%ae-gmbh-4294/jobs',
    #                 'https://www.stepstone.de/cmp/de/igus%c2%ae-gmbh-4294/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/acadevo-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/iu-internationale-hochschule-97654/jobs',
    #                 'https://www.stepstone.de/cmp/de/krongaard-gmbh-77857/jobs',
    #                 'https://www.stepstone.de/cmp/de/perm4-%7c-permanent-recruiting-gmbh-180133/jobs',
    #                 'https://www.stepstone.de/cmp/de/rico-design-gmbh-%26-co-kg-37860/jobs',
    #                 'https://www.stepstone.de/cmp/de/idv-import-und-direkt-vertriebsgmbh-319245/jobs',
    #                 'https://www.stepstone.de/cmp/de/crealogix-112797/jobs',
    #                 'https://www.stepstone.de/cmp/de/amz-stuttgart-gmbh-293489/jobs',
    #                 'https://www.stepstone.de/cmp/de/lobster-experience-gmbh-%26-co-kg-159390/jobs',
    #                 'https://www.stepstone.de/cmp/de/lange-uhren-gmbh-58489/jobs',
    #                 'https://www.stepstone.de/cmp/de/weylchem-performance-products-gmbh-203745/jobs',
    #                 'https://www.stepstone.de/cmp/de/databyte-gmbh-27971/jobs',
    #                 'https://www.stepstone.de/cmp/de/chep-deutschland-gmbh-3250/jobs',
    #                 'https://www.stepstone.de/cmp/de/best-practice-consulting-ag-164161/jobs',
    #                 'https://www.stepstone.de/cmp/de/vetroelite-spa-288248/jobs',
    #                 'https://www.stepstone.de/cmp/de/fenchem-biochemie-gmbh-214378/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/mpdv-mikrolab-gmbh-2961/jobs',
    #                 'https://www.stepstone.de/cmp/de/otto-korsuk%c3%a9witz-gmbh-61615/jobs',
    #                 'https://www.stepstone.de/cmp/de/visable-gmbh-9671/jobs',
    #                 'https://www.stepstone.de/cmp/de/oticon-gmbh-28328/jobs',
    #                 'https://www.stepstone.de/cmp/de/relias-learning-gmbh-172229/jobs',
    #                 'https://www.stepstone.de/cmp/de/k%c3%b6nigsteiner-agentur-gmbh-3478/jobs',
    #                 'https://www.stepstone.de/cmp/de/apollo-optik-holding-gmbh-%26-co-kg-4727/jobs',
    #                 'https://www.stepstone.de/cmp/de/engie-deutschland-gmbh-32815/jobs',
    #                 'https://www.stepstone.de/cmp/de/magna-94465/jobs',
    #                 'https://www.stepstone.de/cmp/de/leomedia-gmbh-92295/jobs',
    #                 'https://www.stepstone.de/cmp/de/shz-schleswig-holsteinischer-zeitungsverlag-gmbh-%26-co-kg-90923/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/shz-schleswig-holsteinischer-zeitungsverlag-gmbh-%26-co-kg-90923/jobs',
    #                 'https://www.stepstone.de/cmp/de/cannamedical-pharma-gmbh-188145/jobs',
    #                 'https://www.stepstone.de/cmp/de/t%c3%9cv-rheinland-group-46685/jobs',
    #                 'https://www.stepstone.de/cmp/de/falstaff-deutschland-gmbh-143509/jobs',
    #                 'https://www.stepstone.de/cmp/de/mevis-medical-solutions-ag-56653/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/ehrhardt-%2b-partner-group-8101/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/vodafone-deutschland-gmbh-152818/jobs',
    #                 'https://www.stepstone.de/cmp/de/vodafone-deutschland-gmbh-152818/jobs',
    #                 'https://www.stepstone.de/cmp/de/vodafone-deutschland-gmbh-152818/jobs',
    #                 'https://www.stepstone.de/cmp/de/vodafone-deutschland-gmbh-152818/jobs',
    #                 'https://www.stepstone.de/cmp/de/aristo-group-143539/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/jungheinrich-aktiengesellschaft-50975/jobs',
    #                 'https://www.stepstone.de/cmp/de/helukabel%c2%ae-gmbh-78043/jobs',
    #                 'https://www.stepstone.de/cmp/de/thyssenkrupp-schulte-gmbh-19979/jobs',
    #                 'https://www.stepstone.de/cmp/de/mediaprint-infoverlag-gmbh-126743/jobs',
    #                 'https://www.stepstone.de/cmp/de/personalwerk-gmbh-9259/jobs',
    #                 'https://www.stepstone.de/cmp/de/autohaus-j-huber-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/axel-springer-se-regionalvermarktung-175668/jobs',
    #                 'https://www.stepstone.de/cmp/de/regler-systems-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/caicon-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/iltex-gmbh-fabrics-%26-more-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/softwareone-deutschland-gmbh-105257/jobs',
    #                 'https://www.stepstone.de/cmp/de/alpha-chip-electronics-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/statista-gmbh-70120/jobs',
    #                 'https://www.stepstone.de/cmp/de/wilhelm-fricke-se-granit-parts-131478/jobs',
    #                 'https://www.stepstone.de/cmp/de/vodafone-deutschland-gmbh-152818/jobs',
    #                 'https://www.stepstone.de/cmp/de/vodafone-deutschland-gmbh-152818/jobs',
    #                 'https://www.stepstone.de/cmp/de/vodafone-deutschland-gmbh-152818/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/ehg-stahlmetall-odelzhausen-gmbh-172228/jobs',
    #                 'https://www.stepstone.de/cmp/de/german-board-advisors-gmbh-d%c3%bcsseldorf-130739/jobs',
    #                 'https://www.stepstone.de/cmp/de/ing-deutschland-1874/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/pluss-personalmanagement-gmbh-karriere-intern-208366/jobs',
    #                 'https://www.stepstone.de/cmp/de/autohaus24-gmbh-318020/jobs',
    #                 'https://www.stepstone.de/cmp/de/sikora-ag-80977/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/tricoma-ag-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/smavesto-gmbh-253976/jobs',
    #                 'https://www.stepstone.de/cmp/de/perfect-production-gmbh-161909/jobs',
    #                 'https://www.stepstone.de/cmp/de/berendsohn-aktiengesellschaft-2159/jobs',
    #                 'https://www.stepstone.de/cmp/de/medical-airport-service-gmbh-281084/jobs',
    #                 'https://www.stepstone.de/cmp/de/xingu-advertising-gmbh-282916/jobs',
    #                 'https://www.stepstone.de/cmp/de/kawasaki-motors-europe-nv-297892/jobs',
    #                 'https://www.stepstone.de/cmp/de/landgard-nord-obst-%26-gem%c3%bcse-gmbh-%26-co-kg-204978/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/datagroup-38117/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/phs-group-269505/jobs',
    #                 'https://www.stepstone.de/cmp/de/phs-group-269505/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/b%c3%bchler-alzenau-gmbh-153246/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/mounting-systems-gmbh-313828/jobs',
    #                 'https://www.stepstone.de/cmp/de/phs-group-269505/jobs',
    #                 'https://www.stepstone.de/cmp/de/solua-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/phs-group-269505/jobs',
    #                 'https://www.stepstone.de/cmp/de/wiegmann-%26-duhn-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/etengo-ag-69561/jobs',
    #                 'https://www.stepstone.de/cmp/de/messe-d%c3%bcsseldorf-gmbh-92113/jobs',
    #                 'https://www.stepstone.de/cmp/de/georg-r%c3%bcgamer-gmbh-270573/jobs',
    #                 'https://www.stepstone.de/cmp/de/calzedonia-germany-gmbh-94454/jobs',
    #                 'https://www.stepstone.de/cmp/de/e-%26-g-real-estate-gmbh-159563/jobs',
    #                 'https://www.stepstone.de/cmp/de/visoon-video-impact-gmbh-%26-co-kg-123361/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-deutsche-st%c3%a4dte-medien-gmbh-100626/jobs',
    #                 'https://www.stepstone.de/cmp/de/ada-learning-gmbh-256926/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/dcon-software-%26-service-ag-6299/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-deutsche-st%c3%a4dte-medien-gmbh-100626/jobs',
    #                 'https://www.stepstone.de/cmp/de/k%c3%b6nigsteiner-agentur-gmbh-3478/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-deutsche-st%c3%a4dte-medien-gmbh-100626/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-deutsche-st%c3%a4dte-medien-gmbh-100626/jobs',
    #                 'https://www.stepstone.de/cmp/de/arthrex-gmbh-3806/jobs',
    #                 'https://www.stepstone.de/cmp/de/dlubal-software-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/woltmann-gmbh-%26-co-kg-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/snapaddy-gmbh-318075/jobs',
    #                 'https://www.stepstone.de/cmp/de/loxone-germany-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/usu-gmbh-5540/jobs',
    #                 'https://www.stepstone.de/cmp/de/smartstreamtv-gmbh-215708/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/gmund-papier-4249/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/uniki-gmbh-177678/jobs',
    #                 'https://www.stepstone.de/cmp/de/mondi-eschenbach-gmbh-120571/jobs',
    #                 'https://www.stepstone.de/cmp/de/skr-reisen-gmbh-91139/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/workwise-gmbh-191177/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/variomeat-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/hilti-deutschland-ag-26563/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/plath-gmbh-%26-co-kg-261447/jobs',
    #                 'https://www.stepstone.de/cmp/de/avoxa-mediengruppe-deutscher-apotheker-gmbh-128451/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/rdb-plastics-gmbh-95491/jobs',
    #                 'https://www.stepstone.de/cmp/de/stellantis-%26you-deutschland-gmbh-111918/jobs',
    #                 'https://www.stepstone.de/cmp/de/jacob-elektronik-gmbh-180279/jobs',
    #                 'https://www.stepstone.de/cmp/de/michael-page-48681/jobs',
    #                 'https://www.stepstone.de/cmp/de/michael-page-48681/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/personalwerk-gmbh-9259/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/michael-page-48681/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/michael-page-48681/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/traser-software-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/autohaus-ernst-gmbh-%26-co-kg-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/bosch-gruppe-2804/jobs',
    #                 'https://www.stepstone.de/cmp/de/2m-deutschland-gmbh-206417/jobs',
    #                 'https://www.stepstone.de/cmp/de/red-bull-deutschland-gmbh-126155/jobs',
    #                 'https://www.stepstone.de/cmp/de/michael-page-48681/jobs',
    #                 'https://www.stepstone.de/cmp/de/michael-page-48681/jobs',
    #                 'https://www.stepstone.de/cmp/de/michael-page-48681/jobs',
    #                 'https://www.stepstone.de/cmp/de/michael-page-48681/jobs',
    #                 'https://www.stepstone.de/cmp/de/mondi-bad-rappenau-gmbh-79988/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/bosch-gruppe-2804/jobs',
    #                 'https://www.stepstone.de/cmp/de/skr-reisen-gmbh-91139/jobs',
    #                 'https://www.stepstone.de/cmp/de/mondi-eschenbach-gmbh-120571/jobs',
    #                 'https://www.stepstone.de/cmp/de/holman-gmbh-296302/jobs',
    #                 'https://www.stepstone.de/cmp/de/str%c3%b6er-media-deutschland-gmbh-25460/jobs',
    #                 'https://www.stepstone.de/cmp/de/fischer-knoblauch-%26-co-medienproduktionsgesellschaft-ffm-mbh-184580/jobs',
    #                 'https://www.stepstone.de/cmp/de/michael-page-48681/jobs',
    #                 'https://www.stepstone.de/cmp/de/sod-screenondemand-gmbh-184676/jobs',
    #                 'https://www.stepstone.de/cmp/de/js-deutschland-gmbh-24984/jobs',
    #                 'https://www.stepstone.de/cmp/de/viscotec-pumpen-u-dosiertechnik-gmbh-49226/jobs',
    #                 'https://www.stepstone.de/cmp/de/viscotec-pumpen-u-dosiertechnik-gmbh-49226/jobs',
    #                 'https://www.stepstone.de/cmp/de/chefs-culinar-nord-gmbh-%26-cokg-201744/jobs',
    #                 'https://www.stepstone.de/cmp/de/haltec-hallensysteme-gmbh-211973/jobs',
    #                 'https://www.stepstone.de/cmp/de/l-mobile-solutions-gmbh-%26-cokg-68896/jobs',
    #                 'https://www.stepstone.de/cmp/de/gruma-nutzfahrzeuge-gmbh-50740/jobs',
    #                 'https://www.stepstone.de/cmp/de/personalwerk-gmbh-9259/jobs',
    #                 'https://www.stepstone.de/cmp/de/accente-gastronomie-service-gmbh-91507/jobs',
    #                 'https://www.stepstone.de/cmp/de/igus%c2%ae-gmbh-4294/jobs',
    #                 'https://www.stepstone.de/cmp/de/k%c3%b6nigsteiner-agentur-gmbh-3478/jobs',
    #                 'https://www.stepstone.de/cmp/de/schneider-electric-gmbh-91666/jobs',
    #                 'https://www.stepstone.de/cmp/de/europaeu-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/salt-and-pepper-technology-gmbh-%26-co-kg-151319/jobs',
    #                 'https://www.stepstone.de/cmp/de/digitalxl-gmbh-%26-co-kg-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/dachser-se-4891/jobs',
    #                 'https://www.stepstone.de/cmp/de/vesterling-ag-6922/jobs',
    #                 'https://www.stepstone.de/cmp/de/b%26k-gmbh-51157/jobs',
    #                 'https://www.stepstone.de/cmp/de/jw-zander-gmbh-%26-cokg-freiburg-ibr-117440/jobs',
    #                 'https://www.stepstone.de/cmp/de/ist-studieninstitut-gmbh-216058/jobs',
    #                 'https://www.stepstone.de/cmp/de/weh-gmbh-verbindungstechnik-180761/jobs',
    #                 'https://www.stepstone.de/cmp/de/lapp-group-7714/jobs',
    #                 'https://www.stepstone.de/cmp/de/home-instead-gmbh-%26-co-kg-112255/jobs',
    #                 'https://www.stepstone.de/cmp/de/bosch-tiernahrung-gmbh-%26-co-kg-159781/jobs',
    #                 'https://www.stepstone.de/cmp/de/finck-%26-claus-gmbh-283977/jobs',
    #                 'https://www.stepstone.de/cmp/de/weischercinema-deutschland-gmbh-%26-cokg-75674/jobs',
    #                 'https://www.stepstone.de/cmp/de/chefs-culinar-nord-gmbh-%26-cokg-201744/jobs',
    #                 'https://www.stepstone.de/cmp/de/innocent-deutschland-gmbh-148816/jobs',
    #                 'https://www.stepstone.de/cmp/de/innocent-deutschland-gmbh-148816/jobs',
    #                 'https://www.stepstone.de/cmp/de/schindler-deutschland-ag-%26-co-kg-4803/jobs',
    #                 'https://www.stepstone.de/cmp/de/qits-gmbh-53663/jobs',
    #                 'https://www.stepstone.de/cmp/de/brandenburg-media-gmbh-%26-co-kg-176547/jobs',
    #                 'https://www.stepstone.de/cmp/de/softwareone-deutschland-gmbh-105257/jobs',
    #                 'https://www.stepstone.de/cmp/de/tempton-intern-247554/jobs',
    #                 'https://www.stepstone.de/cmp/de/horl-1993-gmbh-263308/jobs',
    #                 'https://www.stepstone.de/cmp/de/geze-service-gmbh-53643/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ic-consult-gmbh-229990/jobs',
    #                 'https://www.stepstone.de/cmp/de/testrut-de-gmbh-90868/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/mindsquare-ag-99145/jobs',
    #                 'https://www.stepstone.de/cmp/de/studyflix-gmbh-213191/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/kevox-289843/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/keyence-deutschland-gmbh-6167/jobs',
    #                 'https://www.stepstone.de/cmp/de/greenpocket-gmbh-72152/jobs',
    #                 'https://www.stepstone.de/cmp/de/1%261-versatel-141372/jobs',
    #                 'https://www.stepstone.de/cmp/de/mvi-group-gmbh-112440/jobs',
    #                 'https://www.stepstone.de/cmp/de/gamma-communications-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/multivac-sepp-haggenm%c3%bcller-se-%26-co-kg-186945/jobs',
    #                 'https://www.stepstone.de/cmp/de/aemtec-gmbh-169031/jobs',
    #                 'https://www.stepstone.de/cmp/de/asambeauty-gmbh-137712/jobs',
    #                 'https://www.stepstone.de/cmp/de/red-bull-deutschland-gmbh-126155/jobs',
    #                 'https://www.stepstone.de/cmp/de/dfs-aviation-services-gmbh-178840/jobs',
    #                 'https://www.stepstone.de/cmp/de/1%261-versatel-141372/jobs',
    #                 'https://www.stepstone.de/cmp/de/qualitas-energy-deutschland-gmbh-215709/jobs',
    #                 'https://www.stepstone.de/cmp/de/1%261-versatel-141372/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/kws-group-54038/jobs',
    #                 'https://www.stepstone.de/cmp/de/qualitas-energy-deutschland-gmbh-215709/jobs',
    #                 'https://www.stepstone.de/cmp/de/prodyna-se-22458/jobs',
    #                 'https://www.stepstone.de/cmp/de/infront-b2run-gmbh-159188/jobs',
    #                 'https://www.stepstone.de/cmp/de/dis-ag-29358/jobs',
    #                 'https://www.stepstone.de/cmp/de/growth360-gmbh-288916/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/deutschlandcard-gmbh-55853/jobs',
    #                 'https://www.stepstone.de/cmp/de/krongaard-gmbh-77857/jobs',
    #                 'https://www.stepstone.de/cmp/de/mpdv-mikrolab-gmbh-2961/jobs',
    #                 'https://www.stepstone.de/cmp/de/bike-mobility-services-gmbh-296855/jobs',
    #                 'https://www.stepstone.de/cmp/de/stepstone-gmbh-148733/jobs',
    #                 'https://www.stepstone.de/cmp/de/stepstone-gmbh-148733/jobs',
    #                 'https://www.stepstone.de/cmp/de/stepstone-gmbh-148733/jobs',
    #                 'https://www.stepstone.de/cmp/de/stepstone-gmbh-148733/jobs',
    #                 'https://www.stepstone.de/cmp/de/grefis-hotel-264625/jobs',
    #                 'https://www.stepstone.de/cmp/de/fleetpool-gmbh-146743/jobs',
    #                 'https://www.stepstone.de/cmp/de/netzlink-informationstechnik-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/solcom-gmbh-35805/jobs',
    #                 'https://www.stepstone.de/cmp/de/westwing-group-se-134830/jobs',
    #                 'https://www.stepstone.de/cmp/de/bruker-daltonics-gmbh-%26-co-kg-263251/jobs',
    #                 'https://www.stepstone.de/cmp/de/hensoldt-173428/jobs',
    #                 'https://www.stepstone.de/cmp/de/mast-j%c3%a4germeister-1288/jobs',
    #                 'https://www.stepstone.de/cmp/de/schwarz-dienstleistungen-152212/jobs',
    #                 'https://www.stepstone.de/cmp/de/datatec-ag-119919/jobs',
    #                 'https://www.stepstone.de/cmp/de/vodafone-gmbh-1158/jobs',
    #                 'https://www.stepstone.de/cmp/de/bechtle-gmbh-aachen-164611/jobs',
    #                 'https://www.stepstone.de/cmp/de/convista-consulting-ag-26424/jobs',
    #                 'https://www.stepstone.de/cmp/de/solcom-gmbh-35805/jobs',
    #                 'https://www.stepstone.de/cmp/de/solcom-gmbh-35805/jobs',
    #                 'https://www.stepstone.de/cmp/de/hrbyar-human-resource-solutions-alexander-r%c3%b6hricht-212537/jobs',
    #                 'https://www.stepstone.de/cmp/de/kw-automotive-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/grefis-hotel-264625/jobs',
    #                 'https://www.stepstone.de/cmp/de/solcom-gmbh-35805/jobs',
    #                 'https://www.stepstone.de/cmp/de/riverty-services-gmbh-95244/jobs',
    #                 'https://www.stepstone.de/cmp/de/bechtle-gmbh-aachen-164611/jobs',
    #                 'https://www.stepstone.de/cmp/de/mtu-maintenance-hannover-gmbh-5975/jobs',
    #                 'https://www.stepstone.de/cmp/de/ingenieurgesellschaft-peil_ummenhofer-mbh-153130/jobs',
    #                 'https://www.stepstone.de/cmp/de/deutsche-welle-5128/jobs',
    #                 'https://www.stepstone.de/cmp/de/neoom-germany-gmbh-321729/jobs',
    #                 'https://www.stepstone.de/cmp/de/stepstone-gmbh-148733/jobs',
    #                 'https://www.stepstone.de/cmp/de/eos-holding-96099/jobs',
    #                 'https://www.stepstone.de/cmp/de/lange-uhren-gmbh-58489/jobs',
    #                 'https://www.stepstone.de/cmp/de/skopos-institut-f%c3%bcr-markt-und-kommunikationsforschung-gmbh-%26-co-kg-22421/jobs',
    #                 'https://www.stepstone.de/cmp/de/franken-filtertechnik-kg-275206/jobs',
    #                 'https://www.stepstone.de/cmp/de/tourlane-gmbh-189379/jobs',
    #                 'https://www.stepstone.de/cmp/de/crown-gabelstapler-gmbh-%26-co-kg-139536/jobs',
    #                 'https://www.stepstone.de/cmp/de/lotto-hessen-gmbh-3382/jobs',
    #                 'https://www.stepstone.de/cmp/de/crown-gabelstapler-gmbh-%26-co-kg-139536/jobs',
    #                 'https://www.stepstone.de/cmp/de/prosiebensat1-careers-256089/jobs',
    #                 'https://www.stepstone.de/cmp/de/solcom-gmbh-35805/jobs',
    #                 'https://www.stepstone.de/cmp/de/colibri-beauty-gmbh-187507/jobs',
    #                 'https://www.stepstone.de/cmp/de/paul-hartmann-ag-1906/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/dacoso-gmbh-72665/jobs',
    #                 'https://www.stepstone.de/cmp/de/capmo-gmbh-221200/jobs',
    #                 'https://www.stepstone.de/cmp/de/fenecon-gmbh-%26-co-kg-306847/jobs',
    #                 'https://www.stepstone.de/cmp/de/hess-natur-textilien-gmbh-%26-co-kg-19559/jobs',
    #                 'https://www.stepstone.de/cmp/de/new-work-se-38778/jobs',
    #                 'https://www.stepstone.de/cmp/de/sod-screenondemand-gmbh-184676/jobs',
    #                 'https://www.stepstone.de/cmp/de/pma-tools-ag-180382/jobs',
    #                 'https://www.stepstone.de/cmp/de/solcom-gmbh-35805/jobs',
    #                 'https://www.stepstone.de/cmp/de/arthrex-gmbh-3806/jobs',
    #                 'https://www.stepstone.de/cmp/de/allane-se-62489/jobs',
    #                 'https://www.stepstone.de/cmp/de/t%c3%9cv-rheinland-group-46685/jobs',
    #                 'https://www.stepstone.de/cmp/de/joh-berenberg_gossler-%26-co-kg-275118/jobs',
    #                 'https://www.stepstone.de/cmp/de/gbtec-software-ag-62374/jobs',
    #                 'https://www.stepstone.de/cmp/de/kaffee-partner-gmbh-71684/jobs',
    #                 'https://www.stepstone.de/cmp/de/ericon-gmbh-286317/jobs',
    #                 'https://www.stepstone.de/cmp/de/solcom-gmbh-35805/jobs',
    #                 'https://www.stepstone.de/cmp/de/securepoint-gmbh-251593/jobs',
    #                 'https://www.stepstone.de/cmp/de/softwareone-deutschland-gmbh-105257/jobs',
    #                 'https://www.stepstone.de/cmp/de/ctg-consulting-gmbh-319529/jobs',
    #                 'https://www.stepstone.de/cmp/de/zumtobel-group-34059/jobs',
    #                 'https://www.stepstone.de/cmp/de/statista-gmbh-70120/jobs',
    #                 'https://www.stepstone.de/cmp/de/rewe-group-4036/jobs',
    #                 'https://www.stepstone.de/cmp/de/ntt-data-deutschland-gmbh-107448/jobs',
    #                 'https://www.stepstone.de/cmp/de/dts-systeme-gmbh-26442/jobs',
    #                 'https://www.stepstone.de/cmp/de/studydrive-gmbh-213636/jobs',
    #                 'https://www.stepstone.de/cmp/de/arvato-supply-chain-solutions-se-%e2%80%93-tech-germany-215017/jobs',
    #                 'https://www.stepstone.de/cmp/de/e%26co-consulting-gmbh-288349/jobs',
    #                 'https://www.stepstone.de/cmp/de/ecotel-communication-ag-116733/jobs',
    #                 'https://www.stepstone.de/cmp/de/bertrandt-ag-179/jobs',
    #                 'https://www.stepstone.de/cmp/de/ergotopia-gmbh-262408/jobs',
    #                 'https://www.stepstone.de/cmp/de/baader-bank-ag-83710/jobs',
    #                 'https://www.stepstone.de/cmp/de/continental-ag-3975/jobs',
    #                 'https://www.stepstone.de/cmp/de/orifarm-gmbh-128950/jobs',
    #                 'https://www.stepstone.de/cmp/de/orion-engineered-carbons-gmbh-235532/jobs',
    #                 'https://www.stepstone.de/cmp/de/e-breuninger-gmbh-%26-co-7401/jobs',
    #                 'https://www.stepstone.de/cmp/de/softwareone-deutschland-gmbh-105257/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/securepoint-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/ntt-data-deutschland-gmbh-107448/jobs',
    #                 'https://www.stepstone.de/cmp/de/eclipper-gmbh-253718/jobs',
    #                 'https://www.stepstone.de/cmp/de/medical-airport-service-gmbh-281084/jobs',
    #                 'https://www.stepstone.de/cmp/de/bmw-group-27361/jobs',
    #                 'https://www.stepstone.de/cmp/de/telef%c3%b3nica-germany-gmbh-%26-co-ohg-28299/jobs',
    #                 'https://www.stepstone.de/cmp/de/statista-gmbh-70120/jobs',
    #                 'https://www.stepstone.de/cmp/de/telef%c3%b3nica-germany-gmbh-%26-co-ohg-28299/jobs',
    #                 'https://www.stepstone.de/cmp/de/continental-ag-3975/jobs',
    #                 'https://www.stepstone.de/cmp/de/philipp-gmbh-137380/jobs',
    #                 'https://www.stepstone.de/cmp/de/sthree-gmbh-148920/jobs',
    #                 'https://www.stepstone.de/cmp/de/riani-gmbh-183187/jobs',
    #                 'https://www.stepstone.de/cmp/de/arthrex-gmbh-3806/jobs',
    #                 'https://www.stepstone.de/cmp/de/softing-services-gmbh-82564/jobs',
    #                 'https://www.stepstone.de/cmp/de/sonepar-deutschland-gmbh-30599/jobs',
    #                 'https://www.stepstone.de/cmp/de/man-energy-solutions-se-125579/jobs',
    #                 'https://www.stepstone.de/cmp/de/bechtle-gmbh-it-systemhaus-bonn-k%c3%b6ln-70367/jobs',
    #                 'https://www.stepstone.de/cmp/de/plath-gmbh-%26-co-kg-261447/jobs',
    #                 'https://www.stepstone.de/cmp/de/man-energy-solutions-se-125579/jobs',
    #                 'https://www.stepstone.de/cmp/de/vaillant-deutschland-gmbh-%26-co-kg-203106/jobs',
    #                 'https://www.stepstone.de/cmp/de/motorworld-inn-322489/jobs',
    #                 'https://www.stepstone.de/cmp/de/statista-gmbh-70120/jobs',
    #                 'https://www.stepstone.de/cmp/de/simplicity-networks-gmbh-165095/jobs',
    #                 'https://www.stepstone.de/cmp/de/kistler-instrumente-gmbh-160035/jobs',
    #                 'https://www.stepstone.de/cmp/de/delta-pronatura-dr-krauss-%26-dr-beckmann-kg-52629/jobs',
    #                 'https://www.stepstone.de/cmp/de/dcon-software-%26-service-ag-6299/jobs',
    #                 'https://www.stepstone.de/cmp/de/vitronic-22296/jobs',
    #                 'https://www.stepstone.de/cmp/de/msg-systems-ag-5245/jobs',
    #                 'https://www.stepstone.de/cmp/de/pjur-group-luxembourg-sa-232193/jobs',
    #                 'https://www.stepstone.de/cmp/de/leadec-beteiligungen-gmbh-185132/jobs',
    #                 'https://www.stepstone.de/cmp/de/softwareone-deutschland-gmbh-105257/jobs',
    #                 'https://www.stepstone.de/cmp/de/softwareone-deutschland-gmbh-105257/jobs',
    #                 'https://www.stepstone.de/cmp/de/a-huber-mode-gmbh-321192/jobs',
    #                 'https://www.stepstone.de/cmp/de/magro-verbindungselemente-gmbh-266172/jobs',
    #                 'https://www.stepstone.de/cmp/de/b%c3%bchler-alzenau-gmbh-153246/jobs',
    #                 'https://www.stepstone.de/cmp/de/man-truck-%26-bus-deutschland-gmbh-72760/jobs',
    #                 'https://www.stepstone.de/cmp/de/microsoft-deutschland-gmbh-3107/jobs',
    #                 'https://www.stepstone.de/cmp/de/crealogix-138444/jobs',
    #                 'https://www.stepstone.de/cmp/de/wettercom-gmbh-179295/jobs',
    #                 'https://www.stepstone.de/cmp/de/team-h%26c-talents-der-h%c3%b6chsmann-%26-company-gmbh-%26-co-kg-278339/jobs',
    #                 'https://www.stepstone.de/cmp/de/hahn%2bkolb-werkzeuge-gmbh-89850/jobs',
    #                 'https://www.stepstone.de/cmp/de/radisson-hotel-group-257145/jobs',
    #                 'https://www.stepstone.de/cmp/de/klein-blue-partners-321227/jobs',
    #                 'https://www.stepstone.de/cmp/de/panasonic-industry-europe-gmbh-53790/jobs',
    #                 'https://www.stepstone.de/cmp/de/statista-gmbh-70120/jobs',
    #                 'https://www.stepstone.de/cmp/de/savencia-fromage-%26-dairy-deutschland-gmbh-44384/jobs',
    #                 'https://www.stepstone.de/cmp/de/crown-gabelstapler-gmbh-%26-co-kg-139536/jobs',
    #                 'https://www.stepstone.de/cmp/de/man-energy-solutions-se-125579/jobs',
    #                 'https://www.stepstone.de/cmp/de/mosolf-se-%26-co-kg-240876/jobs',
    #                 'https://www.stepstone.de/cmp/de/page-personnel-55925/jobs',
    #                 'https://www.stepstone.de/cmp/de/solcom-gmbh-35805/jobs',
    #                 'https://www.stepstone.de/cmp/de/eon-impulse-gmbh-289138/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/arvato-systems-gmbh-97750/jobs',
    #                 'https://www.stepstone.de/cmp/de/crown-gabelstapler-gmbh-%26-co-kg-139536/jobs',
    #                 'https://www.stepstone.de/cmp/de/willi-elbe-gelenkwellen-gmbh-%26-co-kg-181493/jobs',
    #                 'https://www.stepstone.de/cmp/de/falke-kgaa-36409/jobs',
    #                 'https://www.stepstone.de/cmp/de/crown-gabelstapler-gmbh-%26-co-kg-139536/jobs',
    #                 'https://www.stepstone.de/cmp/de/bu-power-systems-gmbh-%26-co-kg-129262/jobs',
    #                 'https://www.stepstone.de/cmp/de/nobilis-group-gmbh-68225/jobs',
    #                 'https://www.stepstone.de/cmp/de/ipaxx-ag-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/ipaxx-ag-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/unp-software-gmbh-56470/jobs',
    #                 'https://www.stepstone.de/cmp/de/bundesverband-digitale-wirtschaft-bvdw-ev-216096/jobs',
    #                 'https://www.stepstone.de/cmp/de/techem-energy-services-gmbh-91885/jobs',
    #                 'https://www.stepstone.de/cmp/de/golding-capital-partners-gmbh-26360/jobs',
    #                 'https://www.stepstone.de/cmp/de/cmf-advertising-gmbh-202911/jobs',
    #                 'https://www.stepstone.de/cmp/de/solcom-gmbh-35805/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeitfracht-medien-gmbh-248794/jobs',
    #                 'https://www.stepstone.de/cmp/de/karcher-gmbh-59318/jobs',
    #                 'https://www.stepstone.de/cmp/de/prezero-stiftung-%26-co-kg-257977/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/t%c3%9cv-s%c3%9cd-54474/jobs',
    #                 'https://www.stepstone.de/cmp/de/peek-%26-cloppenburg-kg_d%c3%bcsseldorf-4968/jobs',
    #                 'https://www.stepstone.de/cmp/de/prezero-service-mitte-west-gmbh-%26-co-kg-276810/jobs',
    #                 'https://www.stepstone.de/cmp/de/nordwest-industrie-group-gmbh-167756/jobs',
    #                 'https://www.stepstone.de/cmp/de/drees-%26-sommer-se-3440/jobs',
    #                 'https://www.stepstone.de/cmp/de/softwareone-deutschland-gmbh-105257/jobs',
    #                 'https://www.stepstone.de/cmp/de/ipaxx-ag-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/samsung-sdi-europe-gmbh-100767/jobs',
    #                 'https://www.stepstone.de/cmp/de/first-solar-gmbh-55219/jobs',
    #                 'https://www.stepstone.de/cmp/de/sayway-gmbh-167717/jobs',
    #                 'https://www.stepstone.de/cmp/de/m2c-deutschland-gmbh-285098/jobs',
    #                 'https://www.stepstone.de/cmp/de/wyndham-hannover-atrium-277926/jobs',
    #                 'https://www.stepstone.de/cmp/de/shell-catalyst-%26-technologies-leuna-gmbh-312577/jobs',
    #                 'https://www.stepstone.de/cmp/de/aifinyo-ag-226798/jobs',
    #                 'https://www.stepstone.de/cmp/de/hammers-%26-heinz-immobilien-gmbh-210078/jobs',
    #                 'https://www.stepstone.de/cmp/de/trafineo-gmbh-%26-co-kg-118463/jobs',
    #                 'https://www.stepstone.de/cmp/de/sfc-energy-ag-24963/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/man-truck-%26-bus-deutschland-gmbh-72760/jobs',
    #                 'https://www.stepstone.de/cmp/de/campaign-services-offenbach-gmbh-205678/jobs',
    #                 'https://www.stepstone.de/cmp/de/1%261-versatel-141372/jobs',
    #                 'https://www.stepstone.de/cmp/de/man-truck-%26-bus-deutschland-gmbh-72760/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/arthrex-gmbh-3806/jobs',
    #                 'https://www.stepstone.de/cmp/de/dis-ag-29358/jobs',
    #                 'https://www.stepstone.de/cmp/de/mvi-group-gmbh-112440/jobs',
    #                 'https://www.stepstone.de/cmp/de/1%261-versatel-141372/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/aemtec-gmbh-169031/jobs',
    #                 'https://www.stepstone.de/cmp/de/infront-b2run-gmbh-159188/jobs',
    #                 'https://www.stepstone.de/cmp/de/1%261-versatel-141372/jobs',
    #                 'https://www.stepstone.de/cmp/de/asambeauty-gmbh-137712/jobs',
    #                 'https://www.stepstone.de/cmp/de/1%261-versatel-141372/jobs',
    #                 'https://www.stepstone.de/cmp/de/gamma-communications-gmbh-253207/jobs',
    #                 'https://www.stepstone.de/cmp/de/dfs-aviation-services-gmbh-178840/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/taxdoo-gmbh-240030/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/alsitan-gmbh-80598/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/wisag-geb%c3%a4udereinigung-holding-gmbh-%26-co-kg-174997/jobs',
    #                 'https://www.stepstone.de/cmp/de/dr-johannes-heidenhain-gmbh-6219/jobs',
    #                 'https://www.stepstone.de/cmp/de/control-expert-gmbh-40994/jobs',
    #                 'https://www.stepstone.de/cmp/de/strategy-%26-action-international-gmbh-25542/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/zeit-verlagsgruppe-51847/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/bearingpoint-gmbh-19656/jobs',
    #                 'https://www.stepstone.de/cmp/de/ferchau-gmbh-6095/jobs',
    #                 'https://www.stepstone.de/cmp/de/handelsblatt-gmbh-122959/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/check24-112642/jobs',
    #                 'https://www.stepstone.de/cmp/de/atoss-software-ag-4611/jobs',
    #                 'https://www.stepstone.de/cmp/de/aviareps-tourism-gmbh-84425/jobs',
    #                 'https://www.stepstone.de/cmp/de/arval-deutschland-gmbh-23231/jobs',
    #                 'https://www.stepstone.de/cmp/de/sopra-steria-3313/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/pwc-strategy%26-germany-gmbh-1416/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs',
    #                 'https://www.stepstone.de/cmp/de/11880-internet-services-ag-39584/jobs',
    #                 'https://www.stepstone.de/cmp/de/ratbacher-gmbh-karriere-bei-ratbacher-195828/jobs']
    print(job_urls)
    for x in job_urls:
        company_urls = get_company_urls(x, proxies=proxies)
        to_csv(company_urls, 'Junior Sales.csv')

if __name__ == '__main__':
    main()