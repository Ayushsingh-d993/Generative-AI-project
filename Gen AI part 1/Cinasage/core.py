from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

from langchain_groq import ChatGroq

load_dotenv()


# Initialize model
model = ChatGroq(model="llama-3.3-70b-versatile")

# Define Movie schema
class Movie(BaseModel):
    title: str 
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

# Parser
parser = PydanticOutputParser(pydantic_object=Movie)

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ('system', """
Extract ALL movies from the paragraph.
Return a list of movies.

{format_instructions}
"""),
    ("human", "{paragraph}")
])

# Input
para = input("Give your paragraph: ")

# Format prompt
final_prompt = prompt.invoke({
    "paragraph": para,
    "format_instructions": parser.get_format_instructions()
})
# Get response
response = model.invoke(final_prompt)
print(response.content)

