from langchain_openai import ChatOpenAI


def rewrite_query(question):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = f"""
You are an AI assistant that improves search queries.

Rewrite the following question to be more specific and detailed for retrieving information from research papers.

Original Question:
{question}

Improved Query:
"""

    response = llm.invoke(prompt)

    return response.content.strip()