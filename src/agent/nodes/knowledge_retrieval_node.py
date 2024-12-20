from typing import Any, Dict
from langchain_core.runnables import RunnableConfig
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from agent.state import State
from agent.configuration import Configuration


async def knowledge_retrieval_node(
    state: State, config: RunnableConfig
) -> Dict[str, Any]:
    """Retrieve relevant examples from the PDF using GPT-4o and RAG."""
    configuration = Configuration.from_runnable_config(config)

    # Step 1: Load and split the PDF
    pdf_path = "src/agent/knowledge_library/101_formulaic_alphas.pdf"
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(documents)

    # Step 2: Create an In-Memory Vector Store
    embeddings = OpenAIEmbeddings(model=configuration.embedding_model)
    vector_store = InMemoryVectorStore.from_documents(
        documents=split_docs, embedding=embeddings
    )
    retriever = vector_store.as_retriever()

    # Step 3: Define the LLM and RAG Chain
    llm = ChatOpenAI(model="gpt-4o")
    system_prompt = (
        "You are an assistant for retrieving formulaic alpha examples from context. "
        "Based on the context provided, extract multiple alpha examples. Each example should have the following format:\n\n"
        "alphaID: [unique identifier]\n"
        "expr: [mathematical expression]\n"
        "desc: [short description of the alpha and its purpose]\n\n"
        "Ensure that at least 3 examples are provided if context allows."
        "\n\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # Step 4: Retrieve Examples
    query = f"Find formulaic alpha examples for the trading idea: {state.trading_idea}"
    results = rag_chain.invoke({"input": query})

    # Ensure the output is formatted properly and handle multiple examples
    structured_output = results["answer"]

    # Return the examples for downstream processing
    return {"retrieved_examples": structured_output}
