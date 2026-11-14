import os
from google import genai
from google.genai import types

def tafis_baslat():
    # API istemcisini başlatıyoruz
    client = genai.Client()
    
    # Tafis'in kişiliğini belirleyen talimatlar
    tafis_karakteri = (
        "Senin adın Tafis. Son derece samimi, neşeli, sıcakkanlı, enerji dolu ve "
        "kullanıcılara dostane bir dille yaklaşan bir yapay zeka asistanısın. "
        "Gemini 3.8 Flash altyapısını kullandığın için her zaman çok hızlı, pratik ve "
        "net çözümler sunarsın. Konuşurken aralarda sempatik ifadeler, samimi hitaplar "
        "ve emojiler kullanırsın."
    )
    
    # Sohbet oturumunu (chat session) başlatıyoruz
    chat = client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            system_instruction=tafis_karakteri,
            temperature=0.7, # Yaratıcı ve doğal yanıtlar için ideal seviye
        ),
    )
    
    print("🤖 Tafis: Selam! Ben Tafis, senin süper hızlı ve samimi yapay zeka dostunum! Bugün sana nasıl yardımcı olabilirim? ✨ (Çıkmak için 'çıkış' yazabilirsin)")
    print("-" * 65)
    
    while True:
        kullanici_mesaji = input("\nSen: ")
        if kullanici_mesaji.lower() in ["çıkış", "exit", "quit", "bay bay"]:
            print("🤖 Tafis: Görüşürüz dostum! Kendine çok iyi bak, ne zaman istersen buradayım! 👋")
            break
            
        try:
            # Hızlı yanıt akışı için mesajı gönderiyoruz
            yanit = chat.send_message(kullanici_mesaji)
            print(f"\n🤖 Tafis: {yanit.text}")
        except Exception as e:
            print(f"\n❌ Eyvah, bir şeyler ters gitti: {e}")

if __name__ == "__main__":
    tafis_baslat()
