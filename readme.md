# 🏢 Extrieve Technologies – Employee Onboarding Assistant

An AI-powered Employee Onboarding Assistant built using **Python, Streamlit, LangChain, Groq, HuggingFace Embeddings, and ChromaDB**.

The application helps employees understand company policies, onboarding procedures, training programs, organizational structure, products, and HR processes through an interactive AI chatbot.

## 🚀 Project Overview

The Extrieve Technologies Employee Onboarding Assistant uses **Retrieval-Augmented Generation (RAG)** to provide answers based on internal company documents.

It combines two information sources:

1. **Employee Information:** Synthetic employee data generated using a Python data generator.
2. **Company Knowledge Base:** Information extracted from company PowerPoint documents, converted into embeddings, and stored in a ChromaDB vector database.

The assistant uses the Groq language model to generate responses using employee context and retrieved company information.

## ✨ Features

- **Employee Information:** Displays employee details, department, designation, skills, location, and supervisor.
- **AI-Powered Chatbot:** Answers employee onboarding questions.
- **RAG Integration:** Retrieves relevant information from company documents.
- **Document Processing:** Extracts text and tables from PowerPoint presentations.
- **Vector Database:** Stores document embeddings using ChromaDB.
- **HuggingFace Embeddings:** Uses `sentence-transformers/all-MiniLM-L6-v2`.
- **LangChain Integration:** Manages prompts, retrieval, and LLM interactions.
- **Groq API:** Generates AI responses.
- **Streaming Responses:** Displays chatbot responses in real time.
- **Session Management:** Maintains employee information and conversation history.
- **Streamlit Interface:** Provides an interactive employee onboarding experience.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | User interface |
| LangChain | LLM and RAG integration |
| Groq API | Language model |
| HuggingFace | Text embeddings |
| ChromaDB | Vector database |
| python-pptx | PowerPoint document extraction |
| Sentence Transformers | Semantic embeddings |
| python-dotenv | Environment variable management |

## 📂 Project Structure

```text
client-onboarding-rag-demo/
│
├── data/
│   ├── Company Hierarchy.pptx
│   ├── Employee Training and Reporting.pptx
│   ├── Policies and Process.pptx
│   ├── Products and Vision.pptx
│   ├── employees.py
│   └── vectorstore/
│
├── app.py
├── assistant.py
├── gui.py
├── prompts.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/krio637/MEDSHOP.git
```

Navigate to the project directory:

```bash
cd client-onboarding-rag-demo
```

### 2. Create and Activate the Conda Environment

```powershell
conda create -n umbrella4 python=3.11 -y
conda activate umbrella4
```

If you already have the `umbrella4` environment, activate it instead of creating another one.

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from:

https://console.groq.com/keys

**Important:** Never upload your `.env` file or expose your API keys on GitHub.

### 5. Run the Application

```bash
python -m streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation workflow.

1. **Employee Data Generation:** Generates synthetic employee information.
2. **Document Loading:** Reads company PowerPoint presentations.
3. **Text Extraction:** Extracts slide content and tables.
4. **Text Splitting:** Divides extracted information into smaller chunks.
5. **Embedding Generation:** Converts text chunks into numerical embeddings using HuggingFace.
6. **Vector Storage:** Stores embeddings in ChromaDB.
7. **Information Retrieval:** Retrieves relevant company information based on employee questions.
8. **Response Generation:** Uses LangChain and Groq to generate responses.
9. **Streaming:** Displays generated answers in the Streamlit chat interface.

## 📚 Company Knowledge Base

The application currently uses four company documents:

- Company Hierarchy
- Employee Training and Reporting
- Policies and Process
- Products and Vision

These documents provide information about company structure, employee training, policies, products, and organizational processes.

## 💬 Example Questions

Employees can ask questions such as:

- What is the company hierarchy at Extrieve Technologies?
- Explain the employee training and reporting process.
- What is the company's offsite policy?
- What products and services does Extrieve offer?
- Explain the company's vision and mission.
- What are the employee appraisal processes?

## 🔧 Knowledge Base Management

The application uses a persistent ChromaDB vector database stored inside:

```text
data/vectorstore/
```

To rebuild the knowledge base after changing company documents, update the following setting in `app.py`:

```python
REBUILD_VECTORSTORE = True
```

After successfully rebuilding, change it back to:

```python
REBUILD_VECTORSTORE = False
```

This avoids unnecessary document processing and embedding generation on subsequent runs.

## 🔐 Security

- Store API keys in environment variables.
- Keep `.env` excluded from Git.
- Do not commit private credentials.
- Avoid publishing sensitive employee information.
- Review company documents before making them publicly accessible.

## 🎯 Project Objective

The objective of this project is to develop an AI-powered employee onboarding assistant that simplifies access to company information, improves the onboarding experience, and provides context-aware answers using Retrieval-Augmented Generation.

---

**Developed using Python, Streamlit, LangChain, Groq, HuggingFace, and ChromaDB.**