import os
from typing import List, Dict
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import MultifieldParser

INDEX_DIR = "faq_index"

# ✅ 更新：添加 english_name 字段以支持中英文搜索
schema = Schema(
    drug=TEXT(stored=True),
    english_name=TEXT(stored=True),
    question=TEXT(stored=True),
    answer=TEXT(stored=True)
)

def build_faq_index(data: List[Dict], index_dir: str = INDEX_DIR):
    """
    构建Whoosh索引（每次重建）
    :param data: List of dicts with drug, english_name, question, answer
    """
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    else:
        for f in os.listdir(index_dir):
            os.remove(os.path.join(index_dir, f))

    ix = create_in(index_dir, schema)
    writer = ix.writer()
    for item in data:
        writer.add_document(
            drug=item['drug'],
            english_name=item.get('english_name', ''),
            question=item['question'],
            answer=item['answer']
        )
    writer.commit()

def search_faq(drug_name: str, index_dir: str = INDEX_DIR, top_k: int = 5) -> List[Dict]:
    """
    支持通过 drug 或 english_name 检索FAQ条目
    """
    ix = open_dir(index_dir)
    parser = MultifieldParser(["drug", "english_name"], schema=ix.schema)
    query = parser.parse(drug_name)
    results = []
    with ix.searcher() as searcher:
        hits = searcher.search(query, limit=top_k)
        for hit in hits:
            results.append({
                "question": hit['question'],
                "answer": hit['answer']
            })
    return results

if __name__ == '__main__':
    from utils.data_loader import load_faq_from_json
    data = load_faq_from_json("../data/sample_data.json")
    build_faq_index(data)
    results = search_faq("Olanzapine")  # ✅ 测试英文名
    for r in results:
        print(r)
