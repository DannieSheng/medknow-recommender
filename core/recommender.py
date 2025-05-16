from retriever.faq_search import search_faq
from pub_med.pubmed_fetcher import fetch_pubmed_abstracts
from utils.english_map import get_english_name
from utils.data_loader import load_faq_from_json
from typing import List, Dict

faq_data = load_faq_from_json("data/sample_data.json")

def generate_recommendations(drug_name: str) -> List[Dict]:
    """
    综合推荐：FAQ + PubMed摘要（自动中英映射）
    """
    results = []
    matched_faqs = [e for e in faq_data if e['drug'] == drug_name or e.get('english_name') == drug_name]
    added_label = False

    for item in matched_faqs:
        if item['question'] and item['answer']:
            results.append({
                "type": "FAQ",
                "question": item['question'],
                "answer": item['answer']
            })
        # drug label
        if not added_label and item.get("label_excerpt"):
            label = item["label_excerpt"]
            results.append({
                "type": "Label",
                "question": f"标签信息 - {label.get('section', '说明段')}",
                "answer": label.get("content", "")
            })
            added_label = True

    # PubMed abstract
    english_query = get_english_name(drug_name)
    paper_results = fetch_pubmed_abstracts(english_query, max_results=3)
    for item in paper_results:
        results.append({
            "type": "Paper",
            "question": item['title'],
            "answer": item['abstract'],
        })

    return results


if __name__ == '__main__':
    merged = generate_recommendations("阿莫西林")
    for r in merged:
        print(f"[{r['type']}] {r['question']}\n→ {r['answer']}\n")
