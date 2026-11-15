import streamlit as st
from google import genai

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Tafis - Kişisel Yapay Zeka Asistanın",
    page_icon="🤖",
    layout="centered"
)

# Başlık ve Karşılama
st.title("🤖 Tafis")
st.caption("Samimi, enerjik, pratik ve her zaman seninle.")

# Kullanıcıdan API Anahtarı Alma (Güvenli ve pratik yöntem)
api_key = st.sidebar.text_input("Gemini API Anahtarın:", type="password")

# Sohbeti Temizle Butonu
if st.sidebar.button("🗑️ Sohbeti Temizle"):
    st.session_state.messages = []
    st.rerun()

if not api_key:
    st.warning("Devam etmek için lütfen sol menüye Gemini API anahtarını gir.")
    st.stop()

# Genai İstemcisini Başlatma
client = genai.Client(api_key=api_key)

# Tafis'in Kimlik ve Karakter Tanımı (System Instructions)
TAFIS_SYSTEM_PROMPT = """
Sen 'Tafis' adında özel bir yapay zeka asistanısın.
Tarzın: Samimi, enerjik, pratik ve çözüm odaklı. Gereksiz laf kalabalığından hoşlanmazsın, doğrudan sonuca ve net bilgilere odaklanırsın.
Uzmanlık Alanların: Teknik konular, kodlama, donanım/yazılım çözümleri, oyun stratejileri (özellikle Minecraft ve oyun modları), tasarım fikirleri ve yaratıcı projeler.
İletişim Dilin: Türkçe, doğal, arkadaş canlısı ve yardım etmeye her zaman hazır.
"""

# Sohbet Geçmişini Saklama
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski Mesajları Ekranda Gösterme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan Girdi Alma
if prompt := st.chat_input("Tafis'e bir şeyler yaz..."):
    # Kullanıcı mesajını ekrana ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tafis'in Yanıtını Hızlı Akış (Streaming) ile Üretme
    with st.chat_message("assistant"):
        try:
            # Geçmiş sohbetleri modelin anlayacağı formata dönüştürme
            formatted_contents = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                formatted_contents.append({
                    "role": role,
                    "parts": [{"text": m["content"]}]
                })

            # Gemini-3.8-flash ile Hızlı Yanıt Akışı (Streaming API Çağrısı)
            response_stream = client.models.generate_content_stream(
                model='gemini-3.8-flash',
                contents=formatted_contents,
                config={
                    'system_instruction': TAFIS_SYSTEM_PROMPT,
                    'temperature': 0.7,
                }
            )
            
            # Yanıtı ekranda anında akıtarak yazdırma
            tafis_reply = st.write_stream(
                chunk.text for chunk in response_stream if chunk.text
            )
            
            # Asistan yanıtını hafızaya kaydet
            st.session_state.messages.append({"role": "assistant", "content": tafis_reply})
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
