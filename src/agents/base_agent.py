# src/agents/base_agent.py
from abc import ABC, abstractmethod
import logging

class BaseAgent(ABC):
    """
    Abstract base class for all agents in the legal research chatbot
    """
    def __init__(self, name):
        """
        Initialize the base agent with a name and logger
        
        Args:
            name (str): Name of the agent
        """
        self.name = name
        self.logger = logging.getLogger(name)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    @abstractmethod
    def process(self, input_data):
        """
        Abstract method to be implemented by specific agents
        
        Args:
            input_data: Input data to be processed
        
        Raises:
            NotImplementedError: If not implemented by child classes
        """
        raise NotImplementedError("Subclass must implement abstract method")
    
    def log_info(self, message):
        """
        Log an informational message
        
        Args:
            message (str): Message to log
        """
        self.logger.info(message)
    
    def log_error(self, message):
        """
        Log an error message
        
        Args:
            message (str): Error message to log
        """
        self.logger.error(message)