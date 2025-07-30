from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from index.shared.settings.config import settings
import tempfile
import os
from index.api.models.pdf import PDFAnswer
from index.infra.llm import ChatGoogleGenerativeAIServices 
from langchain_core.language_models.chat_models import BaseChatModel

class PDFChainServices: 
    @property
    def _llm(self) -> BaseChatModel:
        return ChatGoogleGenerativeAIServices()._client 

    def answer_from_pdf(self, content: bytes, question: str) -> str:
        # Save uploaded content temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        # Load + split PDF text
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        docs = splitter.split_documents(documents)

        # Embed + store into Chroma
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GOOGLE_API_KEY)
        vectordb = Chroma.from_documents(docs, embedding=embeddings)

        # Retrieve context and ask Gemini
        retriever = vectordb.as_retriever()
        context_docs: list[Document] = retriever.get_relevant_documents(question)
        context_text = "\n\n".join(doc.page_content for doc in context_docs)

        prompt = f"""Use the context below to answer the question.
        Return only in the following format:

    Context:
    {context_text}

    Question: {question}

    Answer:"""

        model = self._llm.with_structured_output(PDFAnswer)
        return model.invoke(prompt)
        # Cleanup temp file
        os.remove(tmp_path)

        return result
