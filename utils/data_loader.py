import json
from typing import List, Dict


def load_faq_from_json(path: str) -> List[Dict]:
    """
    从JSON文件中加载所有FAQ条目。
    提取 drug, english_name, question, answer 字段用于FAQ索引。
    """
    with open(path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    faq_entries = []
    for entry in raw_data:
        drug = entry.get("drug", "")
        english_name = entry.get("english_name", "")
        for qa in entry.get("faq", []):
            faq_entries.append({
                "drug": drug,
                "english_name": english_name,
                "question": qa.get("question", ""),
                "answer": qa.get("answer", "")
            })
    return faq_entries


if __name__ == "__main__":
    # 测试读取
    data = load_faq_from_json("../data/sample_data.json")
    for d in data:
        print(d)