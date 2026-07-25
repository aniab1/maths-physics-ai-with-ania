import streamlit as st
from google import genai

# إعداد الصفحة
st.set_page_config(
    page_title="مساعد الرياضيات والفيزياء", page_icon="🧮", layout="centered"
)

st.header("مساعد الرياضيات والفيزياء 👨‍🏫")

# التحقق من وجود مفتاح الـ API في أسرار Streamlit
if "GEMINI_API_KEY" not in st.secrets:
    st.error(
        "الرجاء إضافة مفتاح GEMINI_API_KEY في قسم Secrets لوحة التحكم الخاصة بـ"
        " Streamlit."
    )
    st.stop()

# تهيئة عميل Google GenAI بالمفتاح السري
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# تهيئة الذاكرة المؤقتة للرسائل في المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة على الشاشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال سؤال الطالب أو المستخدم
if prompt := st.chat_input("اكتب مسألتك الرياضية أو الفيزياء هنا..."):
    # تخزين وعرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد باستخدام نموذج gemini-1.5-flash
    try:
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير وحل المسألة..."):

                # إعطاء توجيه تخصصي للذكاء الاصطناعي ليركز على الرياضيات والفيزياء
                system_instruction = (
                    "أنت أستاذ خبير وودود في الرياضيات والفيزياء. "
                    "ساعد المستخدم في حل المسائل وشرح القوانين والخطوات بالتفصيل "
                    "وبأسلوب تعليمي مبسط وواضح."
                )

                # دمج التعليمات مع المحادثة الحالية
                full_prompt = f"{system_instruction}\n\nسؤال المستخدم: {prompt}"

                # الاتصال بالنموذج
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=full_prompt,
                )

                bot_reply = response.text
                st.markdown(bot_reply)

        # حفظ رد المساعد في سجل المحادثة
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )

    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بالنموذج: {e}") 
