import streamlit as st
from google import genai

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="مساعد الرياضيات والفيزياء الذكي",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 مساعد الرياضيات والفيزياء الذكي ⚡")
st.write("استنتاجات منهجية وحلول دقيقة من المبادئ الأولية.")

# مفتاح API الخاص بك
GEMINI_API_KEY = "AQ.Ab8RN6Ky9qwNh2Qo0jl8XH9Aze2KIM5U3RQYGY8CbK7G5wdhMg"

# التوجيه الصارم لضمان الدقة المنطقية والرياضية
SYSTEM_INSTRUCTION = """
أنت خبير متقدم جداً في الرياضيات والفيزياء النظرية والتطبيقية.
عند معالجة والإجابة على أي مسألة أو سؤال:
1. قدم تحليلاً مفهومياً دقيقاً واعتمد على الاستنتاج الرياضي والفيزيائي من المبادئ الأولية (First Principles).
2. ركز على البناء المنطقي والخطوات الاشتقاقية الدقيقة.
3. استخدم LaTeX لتنسيق جميع الرموز والمعادلات الرياضية والفيزيائية:
   - استخدم $ ... $ للمعادلات والرموز المضمنة في النص.
   - استخدم $$ ... $$ للمعادلات والاشتقاقات المكرسة في أسطر مستقلة.
"""

# إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال السؤال من المستخدم
if prompt := st.chat_input("اكتب مسألتك الرياضية أو الفيزيائية هنا..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # تهيئة العميل وتوليد الإجابة
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        with st.chat_message("assistant"):
            with st.spinner("جاري تحليل المسألة واستنتاج الحل..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
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
        