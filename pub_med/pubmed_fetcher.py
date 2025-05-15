import requests
import xml.etree.ElementTree as ET
from typing import List, Dict


def fetch_pubmed_abstracts(drug_name: str, max_results: int = 3) -> List[Dict]:
    """
    使用Entrez API从PubMed获取文献摘要
    :param drug_name: 药品名称（英文最佳）
    :param max_results: 返回的最大文献数
    :return: List of dicts with 'title' and 'abstract'
    """
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    # Step 1: 获取PubMed ID列表
    search_params = {
        "db": "pubmed",
        "term": drug_name,
        "retmax": max_results,
        "retmode": "xml"
    }
    search_resp = requests.get(search_url, params=search_params)
    root = ET.fromstring(search_resp.content)
    id_list = [id_elem.text for id_elem in root.findall(".//Id")]

    if not id_list:
        return []

    # Step 2: 获取摘要内容
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"
    }
    fetch_resp = requests.get(fetch_url, params=fetch_params)
    root = ET.fromstring(fetch_resp.content)

    results = []
    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle") or ""
        abstract = article.findtext(".//AbstractText") or "摘要缺失"
        results.append({"title": title.strip(), "abstract": abstract.strip()})

    return results


if __name__ == '__main__':
    drug = "Olanzapine"
    papers = fetch_pubmed_abstracts(drug)
    for i, p in enumerate(papers):
        print(f"[{i+1}] {p['title']}\n摘要：{p['abstract']}\n")
