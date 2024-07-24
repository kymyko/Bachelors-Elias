from flask import Blueprint, request, jsonify
import json
import re
import random

from app import db
from app.models import Chats

bp = Blueprint('chatbot', __name__)

swear_words = ["damn", "crap", "shit", "fuck", "bitch", "bastard", "asshole", "douche", "dick"]
swear_response = "Please try to keep our conversation respectful! I am here for you. How can I assist you today?"


def load_dataset(file_path):
    with open(file_path, 'r') as f:
        dataset = json.load(f)
    return dataset


dataset = load_dataset('/Users/marachirica/PycharmProjects/mentalhealth/app/datasets/psychologyDATASET.json')


def extract_keywords(prompt):
    keywords = re.findall(r'\b\w+\b', prompt.lower())
    return keywords[:5]


def filter_dataset_by_keywords(dataset, keywords):
    filtered_dataset = dataset
    for keyword in keywords:
        filtered_dataset = [entry for entry in filtered_dataset if keyword in entry['prompt'].lower()]
        if len(filtered_dataset) <= 1:
            break
    return filtered_dataset


def contains_swear_words(prompt):
    for word in swear_words:
        if word in prompt.lower():
            return True
    return False


def get_response(prompt, dataset):
    if contains_swear_words(prompt):
        return swear_response
    keywords = extract_keywords(prompt)
    filtered_dataset = filter_dataset_by_keywords(dataset, keywords)
    if filtered_dataset:
        return random.choice(filtered_dataset)['chosen']
    else:
        return "I'm sorry, I don't have an appropriate response for that. Can you rephrase it please?"


@bp.route('/', methods=['POST'])
def chatbot():
    data = request.json
    prompt = data.get('prompt', '')
    if prompt.lower() in ['bye', 'goodbye', 'see you later', 'farewell']:
        response = "Goodbye friend! Hope to hear good news from you soon!"
        chat_log = {'user_input': prompt, 'ai_response': response}
        chat_entry = Chats(chat_log=chat_log)
        db.session.add(chat_entry)
        db.session.commit()
        return jsonify({'response': response})
    else:
        response = get_response(prompt, dataset)
        return jsonify({"response": response})


@bp.route('/initial', methods=['GET'])
def initial():
    return jsonify({"response": "Hello! I am Elias! How can I assist you today?"})
