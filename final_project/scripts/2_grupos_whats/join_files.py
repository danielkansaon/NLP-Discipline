import json

with open('final_whats_groups1.json', 'r') as f:
    pages = json.load(f)

with open('final_whats_groups2.json', 'r') as f:
    pages2 = json.load(f)

    pages.extend(pages2)
with open('final_whats_groups.json', 'w', encoding='utf-8') as f:
    json.dump(pages, f, ensure_ascii=False, indent=4)