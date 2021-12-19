from requests import get
import random
from lxml import html
import json
import os
import time
import sys

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

def collect_group_data(file_name, file_to_save, pstart):
    file_exist = os.path.exists(file_to_save)

    with open(file_name, 'r') as f:
        lines = json.load(f)

    for i_page in range(pstart, len(lines)):
        groups = lines[i_page]['groups']
        v_groups = []

        for i_group in range(0, len(groups)):
            print("PAGE: {0}/{1}".format(i_page + 1, len(lines)))
            print("GROUP: {0}/{1}".format(i_group + 1, len(groups)))
            print("URL: {0}\n".format(groups[i_group]['link']))

            headers = {'User-Agent': get_random_user_agent()}
            response = get("https://gruposwhats.app/group/304848", headers = headers, verify=False, timeout=30)

            if response.status_code == 404:
                return {"url": groups[i_group]['link'], "error": "page not found"}

            #Try to find whatsaap url
            cleaned_response = response.text.replace('\x00', '')
            parser_to_html = html.fromstring(cleaned_response)
            print('- (1) html collected!')
            
            wpp_link = parser_to_html.xpath('//a[contains(text(),"Entrar no Grupo")]')
            title = parser_to_html.xpath('//h5[@class="card-title"]')
            desc = parser_to_html.xpath('//p[@class="card-text"]')
            category = parser_to_html.xpath('//span[@class="card-category"]/text()')
            group_img = parser_to_html.xpath('//img[@class="card-img-top lazy"]')
            date = parser_to_html.xpath('//p[@class="last-check mb-0"]/strong')

            print('- (2) vectors loaded!')
            # exit()
            
            v_groups.append({
                "link": groups[i_group]['link'],
                "whatsapp_link": wpp_link[0].attrib['data-url'],
                "title": title[0].text,
                "category": category[0],
                "description": desc[0].text,
                "created_date": date[0].text,
                "verified_date": date[1].text,
                "group_img": group_img[0].attrib['data-src']
            })
            #break
            time.sleep(0.8)
            print("DONE!\n")

        with open(file_to_save, 'a+', encoding='utf-8') as f:
            if file_exist == True:
                f.write(',')
            else:
                file_exist = True
            json.dump({
                "page": i_page + 1,
                "groups": v_groups
            }, f, ensure_ascii=False, indent=4)
        
        #exit()

if __name__ == "__main__":
    pstart = int(sys.argv[1:][0]) - 1 if len(sys.argv) > 1 else 0
    collect_group_data('all_whats_groups.json', 'final_whats_groups.json', pstart)
    print('END!')


# f = open(r"html_example_group.html", "r")
# page = f.read()
# whatsapp_url = find_whatsaap_link(page)
# parser_to_html = html.fromstring(page)
# f.close()

# https://stackoverflow.com/questions/1276753/xpath-select-first-element-after-some-other-element
# https://stackoverflow.com/questions/57132196/how-to-get-an-element-with-condition-of-its-child-element
