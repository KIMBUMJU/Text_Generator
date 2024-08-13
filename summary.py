# gpt 3.5의 경우, 최대 4096 토큰 즉, 5000-7500글자(영어 기준 약 10000-15000글자)정도 입력받을 수 있음
import os
from openai import OpenAI
import langdetect

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY 환경 변수를 설정해주세요.")

client = OpenAI(api_key=api_key)

def get_system_instruction(lang):
    if lang == 'ko':
        return "다음 회의 노트를 요약해주세요. 주요 내용을 간략하게 정리하고, 마지막에 추가로 논의가 필요한 사항이나 제안을 포함해주세요."
    else:
        return "Please summarize the following meeting notes. Briefly outline the main points and include any additional points for discussion or suggestions at the end."

def summarize_text(text):
    lang = langdetect.detect(text)
    system_instruction = get_system_instruction(lang)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": text}
        ],
        temperature=0,
        max_tokens=200  # max_tokens 값을 증가시켜 더 많은 내용을 요약하도록 함
    )
    summary = response.choices[0].message.content
    formatted_summary = '\n'.join([sentence.strip() for sentence in summary.split('.') if sentence.strip()])
    return formatted_summary

def translate_text(text, target_lang):
    source_lang = langdetect.detect(text)
    if source_lang == target_lang:
        return text  # 이미 목표 언어인 경우 번역하지 않음

    instruction = f"Translate the following text from {source_lang} to {target_lang}:\n\n{text}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text accurately."},
            {"role": "user", "content": instruction}
        ],
        temperature=0,
        max_tokens=500
    )
    return response.choices[0].message.content

def get_language_name(lang_code):
    language_names = {
        'ko': '한국어', 'en': 'English', 'ja': '日本語', 'zh': '中文',
        'es': 'Español', 'fr': 'Français', 'de': 'Deutsch', 'it': 'Italiano',
        'ru': 'Русский', 'pt': 'Português', 'ar': 'العربية', 'hi': 'हिन्दी'
    }
    return language_names.get(lang_code, lang_code)

def main():
    print("[텍스트 요약 및 번역 시스템]")
    print("요약할 텍스트를 입력해주세요. 만약, 종료를 원한다면 'q'를 입력해주세요.")
    
    while True:
        user_input = input("\n텍스트를 입력하세요: ")
        if user_input.lower() == 'q':
            print("프로그램을 종료합니다.")
            break
        
        summary = summarize_text(user_input)
        print("\n요약 결과:")
        print(summary)
        
        translate_option = input("\n번역을 원하시나요? (y/n): ")
        if translate_option.lower() == 'y':
            target_lang = input("번역할 언어 코드를 입력하세요 (예: ko, en, ja, zh, es, fr): ")
            translated_summary = translate_text(summary, target_lang)
            print(f"\n번역된 요약 ({get_language_name(target_lang)}):")
            print(translated_summary)

if __name__ == "__main__":
    main()