from requests import get
import random
from lxml import html
import json
import os
import time
import sys
import datetime

def get_random_user_agent():
    user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
                       'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36']
    return random.choice(user_agent_list)


def collect_links_main_page(baseurl, file_name, pstart, npages):
    file_exist = os.path.exists(file_name)

    for i_page in range(pstart, npages):
        print("PAGE: ", i_page)
        
        # headers = {'User-Agent': get_random_user_agent()}
        # url = baseurl + "?page=" + str(i_page)
        # response = get(url, headers = headers, verify=False, timeout=30)

        # if response.status_code == 404:
        #     return {"url": url, "error": "page not found"}

        # cleaned_response = response.text.replace('\x00', '')
        # parser_to_html = html.fromstring(cleaned_response)

        f = open(r"html_example_group.html", "r")
        page = f.read()
        parser_to_html = html.fromstring(page)
        f.close()

        print('- (1) html collected!')
        v_links = parser_to_html.xpath('//a[contains(text(),"Entrar no Grupo")]')
        v_categoria = parser_to_html.xpath('//span[@class="card-category"]/text()')
        v_title = parser_to_html.xpath('//h5[@class="card-title"]')
        v_desc = parser_to_html.xpath('//p[@class="card-text"]')
        v_group_img = parser_to_html.xpath('//img[@class="card-img-top lazy"]')

        print('- (2) vectors loaded!')
        v_groups = []
        
        for i in range(0, len(v_links)):
            print("- Group: {0}/{1}".format(i+1, len(v_links)))

            v_groups.append({
                "link": v_links[i].attrib['href'],
                "title": v_title[i].text,
                "category": v_categoria[i].strip(),
                "description": v_desc[i].text,
                "created_date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "group_img": v_group_img[i].attrib['data-src']
            })

        print("DONE!\n")

        with open(file_name, 'a+', encoding='utf-8') as f:
            if file_exist == True:
                f.write(',')
            else:
                file_exist = True

            json.dump({
                "page": i_page,
                "groups": v_groups
            }, f, ensure_ascii=False, indent=4)
        
        time.sleep(0.8)

if __name__ == "__main__":
    pstart = int(sys.argv[1:][0]) if len(sys.argv) > 1 else 1

    print(pstart)
    collect_links_main_page("https://gruposwhats.app/", "all_whats_groups.json", pstart, 2)#8791
    print('END!')


# f = open(r"html_example.html", "r")
# page = f.read()
# parser_to_html = html.fromstring(page)
# f.close()

# https://stackoverflow.com/questions/1276753/xpath-select-first-element-after-some-other-element
# https://stackoverflow.com/questions/57132196/how-to-get-an-element-with-condition-of-its-child-element
