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


def collect_links_main_page(baseurl, file_name, pstart, npages):
    file_exist = os.path.exists(file_name)

    for i_page in range(pstart, npages):
        print("PAGE: ", i_page)
        
        headers = {'User-Agent': get_random_user_agent()}
        url = baseurl + "/page" + str(i_page)
        response = get(url, headers = headers, verify=False, timeout=30)

        if response.status_code == 404:
            return {"url": url, "error": "page not found"}

        cleaned_response = response.text.replace('\x00', '')
        parser_to_html = html.fromstring(cleaned_response)

        print('- (1) html collected!')
        v_links = parser_to_html.xpath('//div[@id="botao-participar"]/a')
        v_title = [i.strip() for i in parser_to_html.xpath('//div[@class="single-title-conteudo"]/text()') if i.strip() != '']
        v_desc = parser_to_html.xpath('//p[@class="text-desc"]')
        v_categoria = parser_to_html.xpath('//p[contains(text(),"Categoria:")]/following-sibling::p/a')
        v_vis = parser_to_html.xpath('//span[@class="msg_eye"]/span/text()')
        #v_status = parser_to_html.xpath('//span[contains(text(),"Grupo")]')
        v_date = parser_to_html.xpath('//p[contains(text(),"Adicionado em:")]/following-sibling::p')
        v_fav = parser_to_html.xpath('//span[@class="count-fav"]')
        v_group_img = parser_to_html.xpath('//div[@class="group-imgz"]')

        print('- (2) vectors loaded!')
        v_groups = []

        for i in range(0, len(v_links)):
            print("- Group: {0}/{1}".format(i+1, len(v_links)))

            # Description
            desc_child = list(v_desc[i])
            desc = v_desc[i].text if len(desc_child) == 0 else desc_child[0].text

            # Status
            #is_private = False if v_status[i].text.lower() == 'grupo aberto' else True

            # Date
            date_child = list(v_date[i])
            date = v_date[i].text if len(
                date_child) == 0 else date_child[0].text

            v_groups.append({
                "link": v_links[i].attrib['href'],
                #"title": v_title[i].strip(),
                "category": v_categoria[i].text.strip(),
                "category_url": v_categoria[i].attrib['href'],
                "description": desc,
                "created_date": date,
                #"private": is_private,
                "num_visualization": v_vis[i],
                "num_fav": v_fav[i].text,
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
        
        time.sleep(4)

if __name__ == "__main__":
    pstart = int(sys.argv[1:][0]) if len(sys.argv) > 1 else 1

    print(pstart)
    collect_links_main_page("https://gruposdezap.com/", "all_zap_groups.json", pstart, 2099)#2099
    print('END!')


# f = open(r"html_example.html", "r")
# page = f.read()
# parser_to_html = html.fromstring(page)
# f.close()

# https://stackoverflow.com/questions/1276753/xpath-select-first-element-after-some-other-element
# https://stackoverflow.com/questions/57132196/how-to-get-an-element-with-condition-of-its-child-element
