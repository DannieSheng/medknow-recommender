import csv
from utils.data_loader import load_faq_from_json
import os

# 加载CSV字典
def load_csv_dict(csv_path: str) -> dict:
    mapping = {}
    if not os.path.exists(csv_path):
        return mapping
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            zh = row.get("中文名", "").strip()
            en = row.get("英文名", "").strip()
            if zh and en:
                mapping[zh] = en
    return mapping

# 1. 优先加载 CSV 映射表
csv_map = load_csv_dict("data/drug_dict.csv")

# 2. fallback 加载 sample_data.json
faq_data = load_faq_from_json("data/sample_data.json")


def get_english_name(drug_query: str) -> str:
    """
    药品中文名 → 英文名 映射
    1. 优先查 drug_dict.csv
    2. 再查 sample_data.json
    3. 最后返回原始输入
    """
    if drug_query in csv_map:
        return csv_map[drug_query]

    for entry in faq_data:
        if entry['drug'] == drug_query:
            return entry.get('english_name', drug_query)

    return drug_query


if __name__ == '__main__':
    print(get_english_name("阿莫西林"))     # Amoxicillin
    print(get_english_name("布洛芬"))       # Ibuprofen
    print(get_english_name("Aspirin"))      # Aspirin（英文直接返回）
