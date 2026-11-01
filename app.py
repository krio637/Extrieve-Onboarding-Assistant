import logging
import shutil
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from pptx import Presentation

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

from data.employees import generate_employee_data
from assistant import Assistant
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE
from gui import AssistantGUI


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_PATH = DATA_DIR / "vectorstore"

# Set True for one rebuild, then change back to False.
REBUILD_VECTORSTORE = True


# ==========================================
# 2. STREAMLIT CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Extrieve Technologies | Onboarding Assistant",
    page_icon="https://raw.githubusercontent.com/ExtrieveTechnologies/.github/main/Extrievelogo.png",
    layout="wide"
)


# ==========================================
# 3. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(BASE_DIR / ".env")

logging.basicConfig(level=logging.INFO)


# ==========================================
# 4. LOAD EMPLOYEE INFORMATION
# ==========================================

@st.cache_data(ttl=3600, show_spinner="Loading Employee Data...")
def get_user_data():
    return generate_employee_data(1)[0]


# ==========================================
# 5. INITIALIZE KNOWLEDGE BASE
# ==========================================

@st.cache_resource(show_spinner="Loading Extrieve Knowledge Base...")
def init_vector_store():

    try:

        pptx_files = [
            DATA_DIR / "Employee Training and Reporting.pptx",
            DATA_DIR / "Company Hierarchy.pptx",
            DATA_DIR / "Policies and Process.pptx",
            DATA_DIR / "Products and Vision.pptx",
        ]

        docs = []

        # Extract content from PowerPoint files
        for file_path in pptx_files:

            if not file_path.exists():
                raise FileNotFoundError(
                    f"PowerPoint file not found: {file_path}"
                )

            logging.info(f"Reading document: {file_path.name}")

            presentation = Presentation(str(file_path))

            for slide_number, slide in enumerate(
                presentation.slides, start=1
            ):

                slide_text = []

                for shape in slide.shapes:

                    if shape.has_text_frame:
                        slide_text.append(shape.text)

                    if shape.has_table:

                        for row in shape.table.rows:

                            row_text = " | ".join(
                                cell.text for cell in row.cells
                            )

                            slide_text.append(row_text)

                content = "\n".join(slide_text)

                if content.strip():

                    docs.append(
                        Document(
                            page_content=content,
                            metadata={
                                "source": file_path.name,
                                "slide": slide_number
                            }
                        )
                    )

        if not docs:
            raise ValueError(
                "No text found in company PowerPoint documents."
            )

        logging.info(
            f"Extracted content from {len(docs)} slides."
        )

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )

        splits = text_splitter.split_documents(docs)

        logging.info(
            f"Created {len(splits)} document chunks."
        )

        # Initialize embedding model
        embedding_function = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Remove existing vector database if rebuilding
        if REBUILD_VECTORSTORE and VECTORSTORE_PATH.exists():

            logging.info("Removing old vector database...")

            shutil.rmtree(VECTORSTORE_PATH)

        # Create or load vector database
        if VECTORSTORE_PATH.exists():

            logging.info(
                "Loading existing Extrieve vector database..."
            )

            vectorstore = Chroma(
                persist_directory=str(VECTORSTORE_PATH),
                embedding_function=embedding_function
            )

        else:

            logging.info(
                "Creating new Extrieve vector database..."
            )

            VECTORSTORE_PATH.mkdir(
                parents=True,
                exist_ok=True
            )

            vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=embedding_function,
                persist_directory=str(VECTORSTORE_PATH)
            )

        logging.info(
            "Knowledge base initialized successfully."
        )

        return vectorstore

    except Exception as e:

        logging.exception(
            "Vector store initialization failed."
        )

        st.error(
            f"Failed to initialize knowledge base: {str(e)}"
        )

        return None


# ==========================================
# 6. INITIALIZE APPLICATION
# ==========================================

def main():

    # Load employee information
    customer_data = get_user_data()

    # Load company knowledge base
    vector_store = init_vector_store()

    if vector_store is None:
        st.stop()

    # Initialize session state
    if "customer" not in st.session_state:

        st.session_state.customer = customer_data

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "ai",
                "content": WELCOME_MESSAGE
            }
        ]

    # Initialize Groq LLM
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    # Initialize assistant
    assistant = Assistant(
        system_prompt=SYSTEM_PROMPT,
        llm=llm,
        message_history=st.session_state.messages,
        employee_information=st.session_state.customer,
        vector_store=vector_store
    )

    # Render chatbot interface
    gui = AssistantGUI(assistant)

    gui.render()


# ==========================================
# 7. RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    main()
