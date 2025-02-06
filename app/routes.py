import os
from flask import request, jsonify, render_template
from app import app
from transformers import pipeline
from pydub import AudioSegment
import speech_recognition as sr
import spacy

# Load NLP models
summarizer = pipeline("summarization")
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = [chunk.text for chunk in doc.noun_chunks]
    return keywords

def summarize_text(text, max_length=150, min_length=30):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file_path)
    audio.export("temp.wav", format="wav")
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    os.remove("temp.wav")
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    input_type = request.form.get('input_type')
    max_length = int(request.form.get('max_length', 150))
    min_length = int(request.form.get('min_length', 30))

    if input_type == 'text':
        text = request.form.get('text')
    elif input_type == 'audio':
        audio_file = request.files['audio']
        audio_file_path = os.path.join("uploads", audio_file.filename)
        audio_file.save(audio_file_path)
        text = audio_to_text(audio_file_path)
        os.remove(audio_file_path)
    else:
        return jsonify({"error": "Invalid input type"}), 400

    summary = summarize_text(text, max_length=max_length, min_length=min_length)
    keywords = extract_keywords(text)

    return jsonify({"summary": summary, "keywords": keywords})