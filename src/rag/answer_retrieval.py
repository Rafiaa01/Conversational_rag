from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """
You are an assistant answering questions about an employee policy handbook.

Answer the question using only the context provided.
If the answer is not in the context, say:
"I could not find this information in the employee policy document."

Context:
{context}

Question:
{question}

Answer:
""")


def format_docs(documents):
    return "\n\n".join(
        f"Source: {doc.metadata.get('source')}\n"
        f"Page: {doc.metadata.get('page_number')}\n"
        f"Content: {doc.page_content}"
        for doc in documents
    )


def create_rag_chain(retriever):
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
