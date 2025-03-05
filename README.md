# Indian Legal Research Chatbot

## Overview
A multi-agent AI chatbot designed to provide clear, concise legal information from Indian legal documents.

## Features
- Advanced vector-based document search
- Multi-agent architecture
- Simple legal language generation
- Supports queries about Indian litigation and corporate laws

## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation
1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up `.env` file with OpenAI API key

### Running the Chatbot
```bash
streamlit run app.py
```

## Project Structure
- `src/agents/`: Agent implementations
- `src/knowledge_base/`: Vector database management
- `data/`: Legal document PDFs
- `app.py`: Streamlit application

## Workflow
1. User asks a legal question
2. Query Agent searches relevant documents
3. Summarization Agent simplifies legal text
4. User receives clear, concise response

## Contributing  
Contributions are welcome! Please read the contributing guidelines before making any changes.  

---

## Challenges & Improvements  

### 1. Ensuring Trust & Explainability  
#### 🔴 **Problem:**  
- If the Multi-Agent System (MAS) provides an incorrect or misleading legal summary, users must know **why** that response was chosen.  
- Many multi-agent systems operate as a **black box**, making debugging and justification difficult.  

#### ✅ **Improvements:**  
- Introduce a **Legal Fact-Checker Agent** that cross-verifies claims from different agents.  
- 🔹 Use **confidence scores** to prioritize the most reliable source.  

---

### 2. Conflict Resolution Between Agents  
#### 🔴 **Problem:**  
- If multiple agents return different results (e.g., two sources give conflicting legal interpretations), how does the system **decide which one is correct?**  
- There is no built-in mechanism to handle **inconsistencies** in retrieved legal data.  

#### ✅ **Improvements:**  
- Introduce a **Legal Fact-Checker Agent** that analyzes discrepancies and resolves conflicts.  
- 🔹 Implement **source validation** to rank information based on credibility and legal precedence.  

---

### 3. Optimizing Performance & Efficiency  
#### 🔴 **Problem:**  
- Running agents **sequentially** slows down response times, making the system less efficient.  
- If agents are not managed properly, computational resources can be **wasted**.  

#### ✅ **Improvements:**  
- Instead of running agents **sequentially**, use **asynchronous processing** or **multi-threading** for parallel execution.  
- 🔹 Introduce a **Task Manager** to allocate computing power efficiently and prevent bottlenecks.  

---

💡 **Future Enhancements:**  
✅ Implement **self-learning agents** that improve based on user feedback.  
✅ Develop an **explainability module** that provides reasons for every legal decision.  
✅ Add **multi-modal support** for voice and document-based queries.  
