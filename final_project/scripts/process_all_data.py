
import json
from collections import Counter

excluded_categories = {'fofocas', 'artesanatos', 'lista de transmissão', 
'not found', 'tik tok', 
'youtubers', 'signos', 'nerds', 'imitação', 'trânsito',
'imobiliária', 'compra e venda', 'viagem e turismo', 'investimentos e finanças', 
'tecnologia', 'negócios & empreendedorismo', 'vídeos',
'amizade', 'outros', 'links de grupos', 'links', 'cidades'}


categories =  {'memes, engraçados e zoeira': 'memes engraçados e zoeira',
 'memes, engraçados e zueira': 'memes engraçados e zoeira',
 'figurinhas do whatsapp e stickers': 'figurinhas e stickers',
 'amor': 'amor e romance',
 'saúde, moda e beleza': 'saúde, emagrecimento e beleza',
 'moda e beleza': 'saúde, emagrecimento e beleza',
  'links': 'links de grupos',
  'frases e status': 'frases e mensagens',
  'espiritismo': 'religião',
  'católico': 'religião',
  'gospel': 'religião',
  'videos': 'vídeos',
  'free fire': 'games e jogos',
  'eventos': 'festas, baladas e eventos',
  'festas e baladas': 'festas, baladas e eventos',
  #apos rede
  'vagas de empregos': 'empregos e profissões',
  'profissões': 'empregos e profissões',
  'academia': 'esportes e academia',
  'esportes': 'esportes e academia',
  'namoro': 'amor e romance',
  'concursos': 'educação e estudo',
  'educação': 'educação e estudo',
  'futebol': 'esportes e academia',
  'tv': 'tv, desenhos e animes',
  'desenhos e animes': 'tv, desenhos e animes',
  'emagrecimento e perda de peso': 'saúde, emagrecimento e beleza'
  #'memes, engraçados e zoeira': 'memes engraçados e zoeira'
  #'ganhar dinheiro': 'ganhar dinheiro|investimentos e finanças',
  #'investimentos e finanças': 'ganhar dinheiro|investimentos e finanças'
 }

def json_load(file):
    groups = []
    with open(file, 'r', encoding='utf-8') as w:
        data = json.load(w)
        for p in data:
            for g in p['groups']:
                groups.append(g)

    return groups


file1 = '../scripts/1_grupos_de_zap/data/final_zap_groups.json'
file2 = '../scripts/2_grupos_whats/data/blackbird/final_whats_groups.json'


def get_category_name(categ):
    if categ in categories:
        return categories[categ]
    return categ

def get_uniques_categories(file):

    data = json_load(file)
    all_categories = []
    all_categories = [get_category_name(str(d['category']).lower()) for d in data]
    unique_categories = set(all_categories)

    # print(all_categories)
    print(len(unique_categories))
    return all_categories

def save_clean_data(file, name):
    data = json_load(file)
    clean_data = []
    all_link = set()
    all_desc = []
    count = 0

    for d in data:
        categ = get_category_name(str(d['category']).lower())
        if categ not in excluded_categories:
            desc = str(d['description']).lower()
            count += 1

            if len(desc) > 5:
                all_desc.append(desc)
                l = str(d['whatsapp_link']).lower()
                if l not in all_link:
                    all_link.add(l)
                    
                    clean_data.append({
                        "title": str(d['title']).lower(),
                        "description": desc,
                        "category": categ
                    })

    with open(name, 'w') as f:
        json.dump(clean_data, f, ensure_ascii=False, indent=4)

    print('\nDATASET: ', name)
    print('total groups: ', count)
    print('unique groups whatsaap: ', len(set(all_link)))
    print('unique description: ', len(set(all_desc)))

def count_categories(file):
    with open(file, 'r', encoding='utf-8') as w:
        data = json.load(w)
   
    categs = [str(d['category']).lower() for d in data]
    print(Counter(categs))
    print(len(set(categs)))
    
    return categs

#f1_cat = get_uniques_categories(file1)
#f2_cat = get_uniques_categories(file2)

#unique_categories = {c for c in f2_cat if c not in f1_cat}
#print(unique_categories)
#print(len(unique_categories))

#save_clean_data(file1, './final_data/db_grupos_de_zap.json')
#save_clean_data(file2, './final_data/db_grupos_whats.json')

#cats1 = count_categories('./final_data/db_grupos_de_zap.json')
#cats2 = count_categories('./final_data/db_grupos_whats.json')

# DATASET:  ./final_data/db_grupos_de_zap.json
# total groups:  49530
# unique groups whatsaap:  28319
# unique description:  29116

# DATASET:  ./final_data/db_grupos_whats.json
# total groups:  199248
# unique groups whatsaap:  196583
# unique description:  171263
