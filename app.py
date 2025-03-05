# app.py
import os
import streamlit as st
from dotenv import load_dotenv

# Import agents and knowledge base
from src.knowledge_base.vector_database import VectorDatabase
from src.agents.query_agent import QueryAgent
from src.agents.summarization_agent import SummarizationAgent

# Load environment variables
load_dotenv()

def initialize_chatbot():
    """
    Initialize the multi-agent legal research chatbot
    
    Returns:
        tuple: Initialized query and summarization agents
    """
    # Create vector database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PDF_DIR = os.path.join(BASE_DIR, "data")
    
    pdfs = [
        os.path.join(PDF_DIR, "Guide_to_Litigation.pdf"),
        os.path.join(PDF_DIR, "Legal_Compliance.pdf")
    ]
    
    # Initialize vector database
    vector_db = VectorDatabase()
    vector_db.load_pdfs(pdfs)
    
    # Create agents
    query_agent = QueryAgent(vector_db)
    summarization_agent = SummarizationAgent()
    
    return query_agent, summarization_agent

def main():
    """
    Streamlit application for legal research chatbot
    """
    st.title("🏛️ India's Legal Information Chatbot ")
    
    # Initialize chatbot agents
    query_agent, summarization_agent = initialize_chatbot()
    
    # User input
    user_query = st.text_input(
        "Ask a legal question about Indian law:", 
        placeholder="What are the steps to file a lawsuit in India?"
    )
    
    if st.button("Get Legal Insights"):
        if user_query:
            # Query relevant legal information
            with st.spinner("Searching legal documents..."):
                relevant_sections = query_agent.process(user_query)
            
            # Generate summary
            with st.spinner("Simplifying legal information..."):
                summary = summarization_agent.process(relevant_sections)
            
            # Display results
            st.subheader("Legal Insights")
            st.write(summary)
            
            # Optional: Show source sections
            with st.expander("See Source Sections"):
                for section in relevant_sections:
                    st.text(section)
        else:
            st.warning("Please enter a legal question.")

if __name__ == "__main__":
    main()
