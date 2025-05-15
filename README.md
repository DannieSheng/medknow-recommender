# MedKnowRecommender（Medical Knowledge Recommender）

这是一个轻量级的医药知识推荐系统 Demo，支持用户输入药品名，系统检索出相关的 FAQ 问答内容，并通过大语言模型生成摘要解释。

## ✅ 功能简介
- 从结构化药品FAQ数据中构建检索索引（Whoosh）
- 用户输入药品名后，系统返回匹配FAQ
- 调用大语言模型（如OpenAI GPT）生成总结解释

## 📦 使用说明

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 设置 OpenAI API Key（或替换为你自己的模型接口）
```bash
export OPENAI_API_KEY=your_key_here
```

### 3. 运行主程序
```bash
python app_backend_demo.py
```

### 4. 示例输入
```
药品名: 奥氮平
```
系统将输出推荐问答及解释。

## 🗂️ 数据来源说明
当前项目使用手动构造的小样本数据（`data/sample_data.json`），包含5种常用药品的信息：
- 奥氮平（Olanzapine）
- 帕罗西汀（Paroxetine）
- 阿司匹林（Aspirin）
- 美托洛尔（Metoprolol）
- 苯海拉明（Diphenhydramine）

每种药物包含：
- FAQ 问答
- 标签摘要（如不良反应、用法用量）
- 文献摘要（PubMed 风格）

## 📁 项目结构
```
med_know_recommender/
├── data/
│   └── sample_data.json
├── retriever/
│   └── faq_search.py
├── llm_engine/
│   └── summarizer.py
├── utils/
│   └── data_loader.py
├── app_backend_demo.py
├── requirements.txt
└── README.md
```

---

本项目后续将扩展为支持标签文段推荐、文献RAG检索与 Streamlit UI 展示。

欢迎一起共建！🚀
