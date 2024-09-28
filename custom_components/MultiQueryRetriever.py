from typing import Optional, List

from langchain.retrievers.multi_query import MultiQueryRetriever

from langflow.custom import Component

from langflow.inputs import HandleInput, MessageTextInput, MultilineInput

from langflow.io import Output
from langflow.schema import Data
from langflow.helpers.data import docs_to_data


from langchain_core.output_parsers import BaseOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate



class MultiQueryRetrieverComponent(Component):
    display_name = "MultiQueryRetriever"
    description = "Initialize from llm using default template."
    documentation = "https://python.langchain.com/docs/how_to/MultiQueryRetriever/"
    name = "MultiQueryRetriever"
    
    inputs = [
        MultilineInput(
            name="search_query",
            display_name="Query",
            info="Query to be passed as input.",
            input_types=["Message", "Text"],
        ),
        HandleInput(
            name="llm",
            display_name="LLM",
            info="LLM to be passed as input.",
            input_types=["LanguageModel"],
        ),
        HandleInput(name="retriever", display_name="Retriever", input_types=["Retriever"]),
    ]
    
    outputs = [
        Output(display_name="Retrieved Documents", name="documents", method="retrieve_documents"),
    ]
    

    def retrieve_documents(self) -> List[Data]:
        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant. Your task is to generate five 
            different versions of the given user question to retrieve relevant documents from a vector 
            database. By generating multiple perspectives on the user question, your goal is to help
            the user overcome some of the limitations of the distance-based similarity search. 
            Provide these alternative questions separated by newlines.
            Original question: {question}""",
        )
        retriever = MultiQueryRetriever.from_llm(
            retriever=self.retriever, llm=self.llm, prompt=QUERY_PROMPT, include_original=True, parser_key="lines"
        )  # "lines" is the key (attribute name) of the parsed output
        
        if self.search_query and isinstance(self.search_query, str) and self.search_query.strip():
            unique_docs = retriever.invoke(self.search_query)
            data = docs_to_data(unique_docs)
            self.status = data
            
            return data
            
        else:
            return []