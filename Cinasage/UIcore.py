import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
import json

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="🎬 Movie Extractor AI", layout="centered")

# Title
st.title("🎬 Movie Extractor AI")
st.markdown("Extract structured movie data from any paragraph using AI 🚀")

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

# User input
para = st.text_area("✍️ Enter your paragraph here:", height=200)

# Button
if st.button("🚀 Extract Movies"):
    if para.strip() == "":
        st.warning("Please enter a paragraph first!")
    else:
        with st.spinner("Processing..."):
            try:
                final_prompt = prompt.invoke({
                    "paragraph": para,
                    "format_instructions": parser.get_format_instructions()
                })

                response = model.invoke(final_prompt)

                
                try:
                    data = json.loads(response.content)
                    
                    st.success("✅ Movies Extracted Successfully!")

                    # Display nicely
                    for i, movie in enumerate(data, 1):
                        with st.expander(f"🎬 Movie {i}: {movie.get('title', 'N/A')}"):
                            st.write(f"**Release Year:** {movie.get('release_year')}")
                            st.write(f"**Genre:** {', '.join(movie.get('genre', []))}")
                            st.write(f"**Director:** {movie.get('director')}")
                            st.write(f"**Cast:** {', '.join(movie.get('cast', []))}")
                            st.write(f"**Rating:** {movie.get('rating')}")
                            st.write(f"**Summary:** {movie.get('summary')}")

                except:
                    
                    st.code(response.content)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")