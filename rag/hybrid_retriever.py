from typing import List, Any
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document

from rag.bm25_retriever import BM25Retriever


class HybridRetriever(BaseRetriever):

    vector_retriever: Any
    bm25_retriever: Any

    def __init__(self, vectorstore, documents, **kwargs):
        super().__init__(**kwargs)

        object.__setattr__(
            self,
            "vector_retriever",
            vectorstore.as_retriever(search_kwargs={"k": 5})
        )

        object.__setattr__(
            self,
            "bm25_retriever",
            BM25Retriever(documents)
        )

    def _get_relevant_documents(self, query: str) -> List[Document]:

        vector_docs = self.vector_retriever.invoke(query)
        bm25_docs = self.bm25_retriever.get_relevant_documents(query)

        all_docs = vector_docs + bm25_docs

        seen = set()
        unique_docs = []

        for doc in all_docs:
            content = doc.page_content

            if content not in seen:
                unique_docs.append(doc)
                seen.add(content)

        return unique_docs[:8]