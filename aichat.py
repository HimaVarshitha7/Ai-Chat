import google.generativeai as genai
from PyPDF2 import PdfReader
from typing import List, Dict

class GeminiChat:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model)
        self.conversation: List[Dict[str, List[Dict[str, str]]]] = []

    def add_to_history(self, role: str, content: str):
        self.conversation.append({"role": role, "parts": [{"text": content}]})

    def generate_response(self, user_input: str):
        self.add_to_history("user", user_input)
        try:
            response = self.model.generate_content(contents=self.conversation)
            bot_response = response.text
            self.add_to_history("model", bot_response)
            return bot_response
        except Exception as e:
            return f"Error: {str(e)}"

    def clear_history(self):
        self.conversation = []

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return '\n'.join(text)
    except Exception as e:
        return f"Error reading PDF: {e}"

if __name__ == "__main__":
    chatbot = GeminiChat(api_key="AIzaSyBiRuD5rmvmUTVecNY335pC85p3Z81Zj5E")  # Replace with your actual API key

    print("Welcome to the Gemini Chatbot! \nType 'quit' to exit, 'clear' to reset, or 'pdf' to summarize a PDF.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        elif user_input.lower() == "clear":
            chatbot.clear_history()
            print("Conversation cleared.")
            continue
        elif user_input.lower() == "pdf":
            pdf_file = input("Enter the path to the PDF file: ")
            pdf_data = extract_text_from_pdf(pdf_file)
            if pdf_data.startswith("Error"):
                print(pdf_data)
                continue
            chatbot.clear_history()
            chatbot.add_to_history("user", f"Please summarize the following PDF content:\n\n{pdf_data}")
            response = chatbot.generate_response("Summarize the uploaded PDF.")
            print("Chatbot:", response)
            continue

        response = chatbot.generate_response(user_input)
        print("Chatbot:", response)