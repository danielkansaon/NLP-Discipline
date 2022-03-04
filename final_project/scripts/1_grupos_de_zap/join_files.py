import json

with open('final_zap_groups.json', 'r') as f:
    pages = json.load(f)

with open('final_zap_groups.json', 'r') as f:
    pages2 = json.load(f)

    pages.extend(pages2)
with open('_final_processed_zap_groups.json', 'w', encoding='utf-8') as f:
    json.dump(pages, f, ensure_ascii=False, indent=4)