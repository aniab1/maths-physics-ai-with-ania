import os
import streamlit as st
from google import genai

# إعداد واجهة Streamlit
st.set_page_config(page_title="مساعد الرياضيات والفيزياء", page_icon="🤖")
st.title("🤖 مساعد الرياضيات والفيزياء")

# تعليمات النظام الأساسية
SYSTEM_INSTRUCTION = """
أنت معلم خبير ومحترف في مادتي الرياضيات والفيزياء.
قم بتحليل المسائل خطوة بخطوة، وتقديم شروحات دقيقة ومنطقية مع توضيح القوانين المستخدمة.
"""

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال مدخلات المستخدم
if prompt := st.chat_input("اكتب مسألتك الرياضية أو الفيزياء هنا..."):
    # عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # تهيئة العميل وتوليد الإجابة
    try:
        # جلب المفتاح المباشر من Secrets أو بيئة العمل
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        with st.chat_message("assistant"):
            with st.spinner("جاري تحليل المسألة واستنتاج الحل..."):
                response = client.models.generate_content(
                    model='gemini-2-flash',
                    contents=prompt,
                    config={
                        'system_instruction': SYSTEM_INSTRUCTION,
                        'temperature': 0.1
                    }
                )

                output_text = response.text
                st.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})

    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بالنموذج: {str(e)}") 
