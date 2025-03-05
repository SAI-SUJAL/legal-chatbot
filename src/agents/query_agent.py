# src/agents/query_agent.py
from src.agents.base_agent import BaseAgent
from src.knowledge_base.vector_database import VectorDatabase

class QueryAgent(BaseAgent):
    """
    Agent responsible for retrieving relevant legal information
    """
    def __init__(self, vector_database):
        """
        Initialize Query Agent
        
        Args:
            vector_database (VectorDatabase): Vector database for searching
        """
        super().__init__("QueryAgent")
        self.vector_database = vector_database
    
    def process(self, query, top_k=5):
        """
        Process user query and retrieve relevant legal sections
        
        Args:
            query (str): User's legal query
            top_k (int): Number of top results to retrieve
        
        Returns:
            list: Relevant legal document sections
        """
        try:
            # Log the query
            self.log_info(f"Processing query: {query}")
            
            # Perform vector search
            results = self.vector_database.search(query, top_k)
            
            # Log results
            self.log_info(f"Retrieved {len(results)} relevant sections")
            
            return results
        
        except Exception as e:
            self.log_error(f"Query processing failed: {e}")
            return []