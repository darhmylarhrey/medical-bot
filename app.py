import streamlit as st
from transformers import AutoTokenizer, AutoModel
import weaviate
import torch

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")  # Update URL if using Weaviate Cloud

# Load the MedCPT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ncbi/MedCPT-Query-Encoder")
model = AutoModel.from_pretrained("ncbi/MedCPT-Query-Encoder")

# Function to encode query using MedCPT
def encode_query(query):
    inputs = tokenizer(query, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Function to get medical advice
def get_medical_advice(query):
    query_embedding = encode_query(query).tolist()

    response = client.query.get("MedicalData", ["title", "patient"]).with_near_vector({
        "vector": query_embedding,
        "certainty": 0.7
    }).do()

    if not response['data']['Get']['MedicalData']:
        return "No relevant information found. Please refine your query."

    top_result = response['data']['Get']['MedicalData'][0]
    return top_result['title'], top_result['patient']

# Streamlit frontend
st.title('Medical Assistant Chatbot')

user_input = st.text_input('Enter your symptoms or query:')

if st.button('Get Advice'):
    title, patient_info = get_medical_advice(user_input)
    st.write(f"**Title:** {title}")
    st.write(f"**Patient Info:** {patient_info}")