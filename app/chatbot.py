import json

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_path = "/Users/marachirica/PycharmProjects/mentalhealth/chatbot_model"


class Chatbot:
    def __init__(self, model_path):
        def __init__(self, dataset_path):
            with open(dataset_path, 'r') as file:
                self.dataset = json.load(file)

        def get_response(self, prompt):
            for data in self.dataset:
                if any(keyword.lower() in prompt.lower() for keyword in data['prompt'].split()):
                    return data['chosen']
            return "I'm sorry, I don't understand. Can you please elaborate?"


# Initialize chatbot
chatbot = Chatbot('./chatbot_model')
