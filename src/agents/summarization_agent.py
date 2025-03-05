# src/agents/summarization_agent.py
import os
import openai
from src.agents.base_agent import BaseAgent

class SummarizationAgent(BaseAgent):
    """
    Agent responsible for converting complex legal text to simple language
    """
    def __init__(self):
        """
        Initialize Summarization Agent
        """
        super().__init__("SummarizationAgent")
        
        # Load OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY", "")
    
    def process(self, legal_texts):
        """
        Summarize legal texts into simple, understandable language
        
        Args:
            legal_texts (list): List of legal document sections
        
        Returns:
            str: Simplified, concise summary
        """
        try:
            # Combine texts
            combined_text = " ".join(legal_texts)
            
            # Generate summary using GPT
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a legal expert who translates complex legal language into clear, simple terms. "
                                   "Maintain accuracy while making the explanation accessible."
                    },
                    {
                        "role": "user", 
                        "content": f"Simplify and summarize these legal texts: {combined_text}"
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            summary = response.choices[0].message.content
            
            # Log successful summarization
            self.log_info("Successfully generated summary")
            
            return summary
        
        except Exception as e:
            self.log_error(f"Summarization failed: {e}")
            return "Unable to generate a summary of the legal information."
