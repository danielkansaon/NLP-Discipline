import json
import sys

def show_number_links():
    with open('all_zap_groups.json', 'r') as f:
        pages = json.load(f)
        links = []
        count_all_links = 0

        for pg in pages:
            for g in pg['groups']:
                if g['link'] not in links:
                    links.append(g['link'])
                count_all_links += 1

    print('Links Unicos: ', len(links))
    print('Todos Links: ', count_all_links)

def process_final_file():
    with open('final_zap_groups.json', 'r') as f:
        pages = json.load(f)
        wpp_links = []
        all_groups = []

        print('start reading process!')
        for pg in pages:
            for g in pg['groups']:  
                if 'chat.whatsapp' in g['whatsapp_link'] and g['whatsapp_link'] not in wpp_links:
                    all_groups.append(g)
                    wpp_links.append(g['whatsapp_link'].lower())

    with open('final_processed_zap_groups.json', 'w', encoding='utf-8') as f:
        json.dump(all_groups, f, ensure_ascii=False, indent=4)

    with open('final_links_zap_groups.txt','w') as f:
        for link in wpp_links:
            f.writelines(link + '\n')

    print('Groups: ', len(all_groups))
    print('Links WhatsApp: ', len(wpp_links))
    print('END!')

if __name__ == '__main__':
    op = sys.argv[1:][0] if len(sys.argv) > 1 else 'p'

    if op == 's':
        show_number_links()
    else:
        process_final_file()