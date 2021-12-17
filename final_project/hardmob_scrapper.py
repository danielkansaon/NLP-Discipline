from requests import get
import re
import random
from lxml import html
import json
import gzip
from datetime import datetime
import os
import time

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

def get_comments(baseurl):    
    json_comments = []

    for i in range(1, 5):
        processed_comments = []
        headers = {'User-Agent': get_random_user_agent()}

        current_url = "https://www.hardmob.com.br/" + baseurl + "/page" + str(i + 1) 
        response = get(current_url, headers = headers, verify=False, timeout=30)
        
        if response.status_code == 404:
            return {"url": current_url, "error": "page not found"}

        cleaned_response = response.text.replace('\x00', '')
        cleaned_response = response.text.replace('@', '\n')
        parser_to_html = html.fromstring(cleaned_response)    

        #Get comments and post title
        comments = parser_to_html.xpath('//blockquote[@class="postcontent restore "]/text()')
        text_title = parser_to_html.xpath('//a[@title="Recarregar essa Página"]/text()')
        comments = [c for c in comments if c != "\n"]      
            
        #Joining comments
        for c in comments:
            if(len(processed_comments) < 1 or processed_comments[len(processed_comments) - 1][-1:] == '\n'):
                processed_comments.append(c)
            else:
                processed_comments[len(processed_comments) - 1] += " " +  c
        
        #Transform to Json
        for text in processed_comments:  
            text = text.replace("\n","")
            json_comments.append({
                'url': current_url, 'text': text, 'label':''
            })
        time.sleep(3)

    return [{
        'post_title': text_title[0],
        'comments': json_comments
        }]

def core():
    ids_collected = [] 
    urls = []
    ids = []
    
    date = datetime.today().strftime('%Y-%m-%d')       
    for file_name in os.listdir('%s\data' %(os.getcwd())):
        if file_name.endswith(".gz"):                
            ids_collected.append(os.path.splitext(os.path.splitext(file_name)[0])[0].split("_")[-1])

    with open('posts_urls.json') as f:
        file_content = json.load(f)
    
    for data in file_content:            
        if data["id"] not in ids_collected:
            print("collecting: %s" %(data["id"]))
            json_comments =  get_comments(data["link"])
           
            #Salvando tweets filtrados
            with gzip.GzipFile('%s\data\hardmob_%s_%s.json.gz' %(os.getcwd(), date, data["id"]), 'w') as fout:
                json_str = json.dumps(json_comments, indent=4, ensure_ascii=False)
                json_bytes = json_str.encode('utf-8')
                fout.write(json_bytes)
            
            time.sleep(7)
   
if __name__ == '__main__':
    core()
