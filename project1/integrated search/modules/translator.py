# modules/translator.py

from deep_translator import GoogleTranslator

def translate_text_to_korean(text):
    if not text or not isinstance(text, str):
        return text
    
    try:
        # 영어(en) -> 한국어(ko)
        return GoogleTranslator(source='en', target='ko').translate(text)
    except Exception as e:
        print(f"번역 에러: {e}")
        return text