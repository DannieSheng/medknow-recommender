from retriever.faq_search import search_faq
from pub_med.pubmed_fetcher import fetch_pubmed_abstracts
from utils.english_map import get_english_name
from typing import List, Dict


def generate_recommendations(drug_name: str) -> List[Dict]:
    """
    综合推荐：FAQ + PubMed摘要（自动中英映射）
    """
    results = []

    # FAQ：直接用输入名匹配（支持中英文）
    faq_results = search_faq(drug_name)
    for item in faq_results:
        results.append({
            "type": "FAQ",
            "question": item['question'],
            "answer": item['answer']
        })

    # PubMed：转换为英文名再检索
    english_query = get_english_name(drug_name)
    paper_results = fetch_pubmed_abstracts(english_query, max_results=3)
    for item in paper_results:
        results.append({
            "type": "Paper",
            "question": item['title'],
            "answer": item['abstract']
        })

    return results


if __name__ == '__main__':
    merged = generate_recommendations("阿莫西林")
    for r in merged:
        print(f"[{r['type']}] {r['question']}\n→ {r['answer']}\n")
