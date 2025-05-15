import os
from retriever.faq_search import build_faq_index, search_faq
from llm_engine.summarizer import summarize_recommendation
from utils.data_loader import load_faq_from_json

if __name__ == "__main__":
    print("加载样例数据...")
    data = load_faq_from_json("data/sample_data.json")
    print("构建FAQ索引...")
    build_faq_index(data)

    drug_name = input("请输入药品名，例如：奥氮平\n药品名: ")
    faq_results = search_faq(drug_name)
    print("\n推荐FAQ:")
    for i, item in enumerate(faq_results):
        print(f"[{i+1}] {item['question']} -> {item['answer']}")

    print("\nLLM生成摘要解释:")
    summary = summarize_recommendation(drug_name, faq_results)
    print(summary)

"""
📁 目录结构建议：
med_know_recommender/
├── data/
│   └── sample_data.json          # 药品FAQ+标签+文献数据
├── retriever/
│   └── faq_search.py             # 构建索引 + 搜索模块
├── llm_engine/
│   └── summarizer.py             # LLM摘要解释模块
├── utils/
│   └── data_loader.py            # 加载样例数据
├── app_backend_demo.py          # 主程序（测试版本）
├── requirements.txt
└── README.md
"""
