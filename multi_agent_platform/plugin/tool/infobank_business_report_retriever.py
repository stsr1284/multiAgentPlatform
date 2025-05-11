from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from utils.config import settings
from pathlib import Path

vdb_path = Path(__file__).resolve().parent.parent / "tool/data/infobank_business_report"

vector = FAISS.load_local(
    folder_path=vdb_path,
    index_name="index",
    embeddings=OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY),
    allow_dangerous_deserialization=True,
)
retriever = vector.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    name="infobank_business_report_search",
    description="use this tool to search infobank business report information from the PDF document",
)


async def register(registry):
    await registry.register(retriever_tool)
