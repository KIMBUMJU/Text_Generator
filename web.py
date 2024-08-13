from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
import langdetect

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY 환경 변수를 설정해주세요.")

client = OpenAI(api_key=api_key)

def get_system_instruction(lang):
    if lang == 'ko':
        return "다음 회의 노트를 요약해주세요. 주요 내용을 간략하게 정리하고 핵심내용만 포함되도록 요약해주세요."
    else:
        return "Please Summarise your notes from the next meeting. Be brief and summarise to include only the key points."

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
        max_tokens=200  # 예시로 설정된 max_tokens 값
    )
    summary = response.choices[0].message.content

    # 마지막 완전한 문장을 찾아 반환
    sentences = summary.split('.')
    complete_sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    if complete_sentences:
        last_full_stop = summary.rfind('.')  # 마지막 완전한 문장의 마침표 위치 찾기
        formatted_summary = summary[:last_full_stop+1].strip()  # 마지막 완전한 문장까지만 포함
    else:
        formatted_summary = ""

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize')
def summarize():
    return render_template('summarize.html')

@app.route('/translate')
def translate():
    return render_template('translate.html')

@app.route('/process_summary', methods=['POST'])
def process_summary():
    data = request.json
    text = data['text']
    summary = summarize_text(text)
    return jsonify({'summary': summary})

@app.route('/process_translation', methods=['POST'])
def process_translation():
    data = request.json
    text = data['text']
    target_lang = data['target_lang']
    translated_text = translate_text(text, target_lang)
    return jsonify({
        'translated_text': translated_text,
        'target_lang_name': get_language_name(target_lang)
    })

if __name__ == '__main__':
    app.run(debug=True)
