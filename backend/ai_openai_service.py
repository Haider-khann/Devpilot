import os
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class OpenAIService:
    """AI service using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if self.api_key and self.api_key.startswith('sk-'):
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized")
            except Exception as e:
                logger.error(f"Failed to init OpenAI: {e}")
        else:
            logger.warning("No valid OpenAI API key provided")
    
    def chat(self, system_prompt, user_message, max_tokens=500):
        if not self.client:
            return "[AI not available - add OPENAI_API_KEY to .env]"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return f"AI Error: {str(e)}"
    
    def summarize_code(self, code, language="Python"):
        prompt = f"Analyze this {language} code and provide a clear summary:\n\n```{language}\n{code[:3000]}\n```\n\nExplain: 1) What it does 2) Key functions 3) Notable patterns"
        return self.chat("You are an expert code analyst.", prompt)
    
    def improve_code(self, code, instruction=""):
        if instruction:
            prompt = f"Improve this code. Instruction: {instruction}\n\nOriginal:\n```\n{code[:3000]}\n```\n\nProvide improved code in a code block and explain changes."
        else:
            prompt = f"Improve this code. Make it cleaner and follow best practices.\n\nOriginal:\n```\n{code[:3000]}\n```\n\nProvide improved code in a code block and explain changes."
        return self.chat("You are a senior software engineer.", prompt, max_tokens=2000)
    
    def answer_question(self, code, question):
        prompt = f"Given this code:\n```\n{code[:3000]}\n```\n\nQuestion: {question}\n\nProvide a helpful answer."
        return self.chat("You are a helpful coding assistant.", prompt)
    
    def generate_code(self, description, reference_code=""):
        if reference_code:
            prompt = f"Generate new code. Description: {description}\n\nReference code for style:\n```\n{reference_code[:2000]}\n```\n\nProvide the generated code."
        else:
            prompt = f"Generate code. Description: {description}\n\nProvide the code."
        return self.chat("You are a senior developer. Generate clean, working code.", prompt, max_tokens=3000)