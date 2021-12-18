from requests import get
import random
from lxml import html
import json
import os
import time
import sys
import re

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

def find_whatsaap_link(html_text):
    url_whatsapp = "Not Found"

    result = re.findall(r'(".+chat.whatsapp.com.+")', html_text)
    if len(result) > 0:
        print(result[0])
        url_whatsapp = result[0].replace("\"","")
    else:
        result = re.findall(r'(".+api.whatsapp.com.+")', html_text)
        if len(result) > 0:
            print(result[0])
            url_whatsapp = result[0].replace("\"","")
    
    return url_whatsapp

def get_links(file_name, file_to_save, pstart):
    file_exist = os.path.exists(file_to_save)

    with open(file_name, 'r') as f:
        lines = json.load(f)

    for i_page in range(pstart, len(lines)):
        groups = lines[i_page]['groups']
        v_groups = []

        for i_group in range(0, len(groups)):
            print("GROUP: ", i_group + 1)

            headers = {'User-Agent': get_random_user_agent()}
            response = get(groups[i_group]['link'], headers = headers, verify=False, timeout=30)

            if response.status_code == 404:
                return {"url": groups[i_group]['link'], "error": "page not found"}

            #Try to find whatsaap url
            whatsapp_url = find_whatsaap_link(response.text)
            cleaned_response = response.text.replace('\x00', '')
            parser_to_html = html.fromstring(cleaned_response)
            print('- (1) html collected!')
            
            v_title = parser_to_html.xpath('//h1[@class="single-title"]/text()')
            v_desc = parser_to_html.xpath('//p[contains(text(),"Descrição:")]/following-sibling::p')
            v_admin = parser_to_html.xpath('//p[@class="admin"]')
            v_regras = parser_to_html.xpath('//p[contains(text(),"Regras")]/following-sibling::p')
            v_category = parser_to_html.xpath('//p[contains(text(),"Categoria:")]/following-sibling::p/a/text()')
            v_date = parser_to_html.xpath('//p[contains(text(),"Adicionado em:")]/following-sibling::p')

            print('- (2) vectors loaded!')
            # exit()

            #Admin
            adm_child = list(v_admin[0])
            adm = adm_child[1].text if len(adm_child) == 2 else adm_child[0][1].text

            #Date
            date_child = list(v_date[0])
            date = v_date[0].text if len(date_child) == 0 else date_child[0].text

            #Regras
            regras_child = list(v_regras[0])
            regras = v_regras[0].text if len(regras_child) == 0 else regras_child[0].text

            # Description
            desc_child = list(v_desc[0])
            desc = v_desc[0].text if len(desc_child) == 0 else desc_child[0].text
  
            v_groups.append({
                "link": groups[i_group]['link'],
                "whatsapp_link": whatsapp_url,
                "title": "Not Found" if len(v_title) == 0 else v_title[0],
                "admin": "Not Found" if adm == None or len(adm) == 0 else adm,
                "category": "Not Found" if len(v_category) == 0 else v_category[0],
                "category_url": groups[i_group]['category_url'],
                "description": "Not Found" if desc == None or len(desc) == 0 else desc,
                "rules": "Not Found" if regras == None or len(regras) == 0 else regras,
                "created_date": "Not Found" if date == None or len(date) == 0 else date,
                "num_visualization": groups[i_group]['num_visualization'],
                "num_fav": groups[i_group]['num_fav'],
                "group_img": groups[i_group]['group_img']
            })
            
            time.sleep(1)
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

if __name__ == "__main__":
    pstart = int(sys.argv[1:][0]) - 1 if len(sys.argv) > 1 else 0
    get_links('all_zap_groups.json', 'final_zap_groups.json', pstart)
    print('END!')


# f = open(r"html_example_group.html", "r")
# page = f.read()
# parser_to_html = html.fromstring(page)
# f.close()

# https://stackoverflow.com/questions/1276753/xpath-select-first-element-after-some-other-element
# https://stackoverflow.com/questions/57132196/how-to-get-an-element-with-condition-of-its-child-element
