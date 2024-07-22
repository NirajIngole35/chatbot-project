import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import time

# Load corpus from JSON file
def load_corpus_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    questions = []
    answers = []
    for item in data:
        questions.append(item['question'])
        answers.append(item['answer'])
    return questions, answers

# Extract text from PDF
def extract_text_from_pdf(file_path):
    pdf_text = []
    doc = fitz.open(file_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pdf_text.append(page.get_text())
    return ' '.join(pdf_text)

# Load corpus from JSON file
json_file_path = 'Sample Question Answers.json'
questions, answers = load_corpus_from_json(json_file_path)

# Load corpus from PDF file
pdf_file_path = 'corpus.pdf'
pdf_text = extract_text_from_pdf(pdf_file_path)
pdf_sentences = pdf_text.split('. ')  # Simple split, can be improved with better sentence segmentation

# Combine JSON and PDF corpus
combined_questions = questions + pdf_sentences
combined_answers = answers + pdf_sentences  # Using same sentences as answers for simplicity

# Initialize a sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode corpus sentences to get embeddings
corpus_embeddings = model.encode(combined_questions)

class Chatbot:
    def __init__(self, questions, answers, corpus_embeddings, model, threshold=0.5):
        self.questions = questions
        self.answers = answers
        self.corpus_embeddings = corpus_embeddings
        self.model = model
        self.threshold = threshold
        self.conversation_history = []
        self.formalities = {
            "hi": "Hello! How can I assist you today?",
            "hello": "Hi there! How can I help you?",
            "how are you": "I'm just a bot, but I'm here to help you!",
            "hey": "Hey! How can I assist you today?",
        }
    
    def get_response(self, user_query):
        self.conversation_history.append(user_query.lower())
        
        # Check for formalities
        if user_query.lower() in self.formalities:
            return self.formalities[user_query.lower()], 'blue'
        
        user_embedding = self.model.encode([user_query])
        similarities = cosine_similarity(user_embedding, self.corpus_embeddings)
        
        max_similarity = np.max(similarities)
        if max_similarity < self.threshold:
            return "Please contact us directly for more information.", 'pink'
        
        best_match_idx = np.argmax(similarities)
        return self.answers[best_match_idx], 'green'

# Initialize chatbot
chatbot = Chatbot(combined_questions, combined_answers, corpus_embeddings, model)

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Tkinter chat application
class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Wine Chatbot")
        self.geometry("400x500")

        self.chat_history = scrolledtext.ScrolledText(self, state='disabled', wrap=tk.WORD)
        self.chat_history.pack(padx=10, pady=10, expand=True, fill='both')

        self.user_input = tk.Entry(self, width=80)
        self.user_input.pack(padx=10, pady=10, fill='x')

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        self.bind('<Return>', lambda event: self.send_message())

        self.display_message("Bot", "Hi there! How can I help you today?", 'blue')
        speak("Hi there! How can I help you today?")

    def send_message(self):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message("User", user_message, 'red')  # Display user message in red
            self.update()  # Ensure the message is processed
            speak(user_message)
            time.sleep(1)  # Delay before processing bot response

            response, color = chatbot.get_response(user_message)
            self.display_message("Bot", response, color)
            self.update()  # Ensure the response is displayed before speaking
            speak(response)

        self.user_input.delete(0, tk.END)

    def display_message(self, sender, message, color):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, f"{sender}: {message}\n", color)
        self.chat_history.tag_configure(color, foreground=color)
        self.chat_history.configure(state='disabled')
        self.chat_history.yview(tk.END)

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
