import os
import logging

logger = logging.getLogger(__name__)

class GeminiAIService:
    """AI service using Google Gemini API."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                # Use the correct model name for current API
                self.model = genai.GenerativeModel('models/gemini-3.6-flash')
                logger.info("Gemini initialized with gemini-2.0-flash")
            except Exception as e:
                logger.error(f"Init error: {e}")
                self.model = None
    
    def chat(self, system_prompt, user_message, max_tokens=500):
        if not self.model:
            return "[AI not available]"
        try:
            prompt = f"{system_prompt}\n\n{user_message}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"Error: {str(e)[:200]}"
    
    def summarize_code(self, code, language="Python"):
        prompt = f"Analyze this {language} code and provide a summary:\n```\n{code[:3000]}\n```"
        return self.chat("You are an expert code analyst.", prompt)
    
    def improve_code(self, code, instruction=""):
        prompt = f"Improve this code. {instruction}\n\nCode:\n```\n{code[:3000]}\n```\nProvide improved code."
        return self.chat("You are a senior engineer.", prompt, max_tokens=2000)
    
    def answer_question(self, code, question):
        prompt = f"Code:\n```\n{code[:3000]}\n```\n\nQuestion: {question}"
        return self.chat("You are a coding assistant.", prompt)
    
    def generate_code(self, description, reference_code=""):
        prompt = f"Generate code. Description: {description}\n" + (f"Reference:\n```\n{reference_code[:2000]}\n```" if reference_code else "")
        return self.chat("You are a developer. Generate code.", prompt, max_tokens=3000)