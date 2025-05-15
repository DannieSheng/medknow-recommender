import os
from typing import List, Dict
from dotenv import load_dotenv
import openai
load_dotenv()


API_KEY = os.getenv('API_KEY') 
BASE_URL = os.getenv('BASE_URL')  # Get the

client = openai.OpenAI(api_key=API_KEY, 
            base_url=BASE_URL)

def summarize_recommendation(drug: str, faq_items: List[Dict]) -> str:
    """
    使用GPT模型对推荐FAQ生成一段摘要解释。
    """
    if not faq_items:
        return "未找到任何相关问答。"

    content = f"你是一位医学知识助手。请为药品“{drug}”生成一段用户友好的摘要，基于以下问答内容：\n"
    for item in faq_items:
        content += f"\nQ: {item['question']}\nA: {item['answer']}"
    content += "\n请简洁总结这些内容，适合非专业人士理解。"

    try:
        response = client.chat.completions.create(# openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个医学FAQ摘要助手。"},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"调用OpenAI接口失败：{str(e)}"


if __name__ == '__main__':
    test_data = [
        {"question": "奥氮平用于治疗哪些疾病？", "answer": "精神分裂症和双相情感障碍。"},
        {"question": "奥氮平有哪些副作用？", "answer": "体重增加、嗜睡、头晕。"}
    ]
    print(summarize_recommendation("奥氮平", test_data))
