import os
import logging
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

# Wrap Gemini access in one service so API failures do not reach route handlers.
class GeminiAIService:
    """AI service using Google Gemini API."""
    
    def __init__(self, api_key=None):
        """Configure the Gemini client when an API key is available."""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                # Keep model setup in one place so all AI operations share it.
                self.model = genai.GenerativeModel('models/gemini-3.6-flash')
                logger.info("Gemini initialized with gemini-2.0-flash")
            except Exception as e:
                logger.error(f"Init error: {e}")
                self.model = None
    
    def chat(self, system_prompt, user_message, max_tokens=500):
        """Send a prompt to Gemini and return a safe fallback on failure."""
        if not self.model:
            return "[AI not available]"
        try:
            # Combine system guidance and user input into the model prompt.
            prompt = f"{system_prompt}\n\n{user_message}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error: {e}")
            return f"Error: {str(e)[:200]}"
    
    def summarize_code(self, code, language="Python"):
        """Request a concise summary of the supplied source code."""
        prompt = f"Analyze this {language} code and provide a summary:\n```\n{code[:3000]}\n```"
        return self.chat("You are an expert code analyst.", prompt)
    
    def improve_code(self, code, instruction=""):
        """Request an improved version of the supplied source code."""
        prompt = f"Improve this code. {instruction}\n\nCode:\n```\n{code[:3000]}\n```\nProvide improved code."
        return self.chat("You are a senior engineer.", prompt, max_tokens=2000)
    
    def answer_question(self, code, question):
        """Answer a question using the supplied code as context."""
        prompt = f"Code:\n```\n{code[:3000]}\n```\n\nQuestion: {question}"
        return self.chat("You are a coding assistant.", prompt)
    
    def generate_code(self, description, reference_code=""):
        """Generate code from a description and optional reference code."""
        prompt = f"Generate code. Description: {description}\n" + (f"Reference:\n```\n{reference_code[:2000]}\n```" if reference_code else "")
        return self.chat("You are a developer. Generate code.", prompt, max_tokens=3000)