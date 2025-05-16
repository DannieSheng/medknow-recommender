import streamlit as st
from utils.data_loader import load_faq_from_json
from retriever.faq_search import build_faq_index
from core.recommender import generate_recommendations
from llm_engine.summarizer import summarize_recommendation


# initialize data and index
@st.cache_resource
def load_sample_data():
    data = load_faq_from_json("data/sample_data.json")
    return data

st.set_page_config(page_title="MedKnow Recommender", layout="wide")
st.title("🧠 医药推荐与摘要系统")
st.markdown("输入药品名称（中/英文），系统将整合FAQ + PubMed摘要进行推荐，并生成总结解释。")

data = load_sample_data()
build_faq_index(data)

query = st.text_input("请输入药品名称", value="奥氮平")

if query:
    with st.spinner("正在整合推荐与摘要中..."):
        items = generate_recommendations(query)

        if items:
            st.subheader("📚 推荐内容")
            faq_count = 0
            for idx, item in enumerate(items):
                type_lower = item['type'].lower()
                if type_lower== "faq":
                    faq_count += 1
                    label = "[FAQ]"
                elif type_lower == "label":
                    label = "[📄标签]"
                else:
                    label = "[📘文献]"
                with st.expander(f"{label} Q{idx+1}: {item['question']}"):
                    st.markdown(f"**答：** {item['answer']}")

            st.subheader("🧠 LLM 生成总结解释")
            if faq_count > 0:
                llm_input = [
                    {"question": item['question'], "answer": item['answer']}
                    for item in items if item['type'] == "FAQ"
                ]
                summary = summarize_recommendation(query, llm_input)
                st.success(summary)
            else:
                st.info("未检索到本地FAQ问答内容，已展示文献摘要。")
        else:
            st.warning("未找到任何相关内容，请尝试其他药品名。")
else:
    st.info("请输入一个药品名以开始推荐。")
