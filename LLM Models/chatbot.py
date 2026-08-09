from dotenv import load_dotenv
import os
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)

messages = [
    SystemMessage(content="You are a funny AI Agent")
]

print("============= Welcome to AI Chatbot ==============")
print("Type 0 to exit")

while True:
    prompt = input("You: ")
    
    if prompt == "0":
        break

    messages.append(HumanMessage(content=prompt))
    response = model.invoke(messages)

    messages.append(AIMessage(content=response.content))
    print("Bot:", response.content)

print(messages)