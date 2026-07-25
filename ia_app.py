import google.generativeai as genai
import streamlit as st

# إعداد الصفحة
st.set_page_config(
    page_title="مساعد الرياضيات والفيزياء", page_icon="🧮", layout="centered"
)

st.header("مساعد الرياضيات والفيزياء 👨‍🏫")

# التحقق من مفتاح الـ API
if "GEMINI_API_KEY" not in st.secrets:
    st.error(
        "الرجاء إضافة مفتاح GEMINI_API_KEY في قسم Secrets لوحة التحكم الخاصة بـ"
        " Streamlit."
    )
    st.stop()

# إعداد المفتاح
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# تهيئة النموذج المستقر
model = genai.GenerativeModel("gemini-1.5-flash")

# إدارة حالة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال رسالة المستخدم
if prompt := st.chat_input("اكتب مسألتك الرياضية أو الفيزياء هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير وحل المسألة..."):
                # تعليمات تخصصية
                system_instruction = (
                    "أنت أستاذ خبير وودود في الرياضيات والفيزياء. "
                    "ساعد المستخدم في حل المسائل وشرح القوانين والخطوات بالتفصيل."
                )

                full_prompt = f"{system_instruction}\n\nسؤال المستخدم: {prompt}"

                response = model.generate_content(full_prompt)
                bot_reply = response.text
                st.markdown(bot_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )

    except Exception as e:
        st.error(f"حدث خطأ أثنا
