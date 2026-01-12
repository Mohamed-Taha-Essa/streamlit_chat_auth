#langchain operation 
import os
from langchain_huggingface import HuggingFaceEndpoint ,ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory


SYSTEM_PROMPT= "You are a helpfull assistant"


#initialize the chat model
hugging_face_api_key = os.getenv('hugging_face_api_key')
print(hugging_face_api_key)

llm = HuggingFaceEndpoint(
    repo_id="EssentialAI/rnj-1-instruct",
    task="text-generation",
    provider="auto",  # set your provider here
    huggingfacehub_api_token=hugging_face_api_key,
)

# initialize chat model
chat_model = ChatHuggingFace(llm=llm)
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
#create chain 
chain = prompt | chat_model

#only return msgs for only one user when using  lambda session_id :msgs, in all scenario it return the msgs in production 
#system must write get_session_history function
# input_messages_key : is the key that human using in prompt  ("human", "{input}")
# history_messages_key : is the key that sent using     MessagesPlaceholder(variable_name="chat_history"), in prompt
def get_chain_with_history(msgs):
    return RunnableWithMessageHistory(
        chain ,
        lambda session_id :msgs,
        input_messages_key='input',
        history_messages_key='chat_history'
    )