# import json
# from transformers import AutoTokenizer, AutoModel
# import torch

# # Load the MedCPT model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("ncbi/MedCPT-Article-Encoder")
# model = AutoModel.from_pretrained("ncbi/MedCPT-Article-Encoder")

# # Load your dataset
# with open('/Users/dhrey/Desktop/Workspace/NEU/INFO7375/medical-bot/PMC-Patients.json') as f:
#     data = json.load(f)

# # Function to encode text using MedCPT
# def encode_text(text):
#     inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# # Process the dataset
# encoded_data = []
# for item in data:
#     encoded_item = {
#         "patient_id": item["patient_id"],
#         "patient_uid": item["patient_uid"],
#         "PMID": item["PMID"],
#         "file_path": item["file_path"],
#         "title": item["title"],
#         "patient": item["patient"],
#         "age": item["age"],
#         "gender": item["gender"],
#         "relevant_articles": item["relevant_articles"],
#         "similar_patients": item["similar_patients"],
#         "embedding": encode_text(item["patient"]).tolist()
#     }
#     encoded_data.append(encoded_item)

# # Save the encoded data
# with open('encoded_data.json', 'w') as f:
#     json.dump(encoded_data, f)


import json
import torch
from transformers import AutoTokenizer, AutoModel
import weaviate
from tqdm import tqdm  # For progress bar

# Load the MedCPT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ncbi/MedCPT-Article-Encoder")
model = AutoModel.from_pretrained("ncbi/MedCPT-Article-Encoder")

# Load your dataset
with open('/Users/dhrey/Desktop/Workspace/NEU/INFO7375/medical-bot/PMC-Patients.json') as f:
    data = json.load(f)

# Weaviate client setup
client = weaviate.Client("http://localhost:8080")  # Adjust if you're using Weaviate Cloud

# Define the schema for Weaviate
class_obj = {
    "class": "MedicalData",
    "description": "A class to store medical patient data",
    "properties": [
        {"name": "patient_id", "dataType": ["string"]},
        {"name": "patient_uid", "dataType": ["string"]},
        {"name": "PMID", "dataType": ["string"]},
        {"name": "file_path", "dataType": ["string"]},
        {"name": "title", "dataType": ["string"]},
        {"name": "patient", "dataType": ["text"]},
        {"name": "age", "dataType": ["number"]},
        {"name": "gender", "dataType": ["string"]},
        {"name": "relevant_articles", "dataType": ["string[]"]},
        {"name": "similar_patients", "dataType": ["string[]"]},
        {"name": "embedding", "dataType": ["number[]"], "vectorIndexType": "hnsw"}
    ]
}

client.schema.create_class(class_obj)

# Function to encode a batch of texts
def encode_batch(batch_texts):
    inputs = tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

# Process the dataset in batches and upload to Weaviate
batch_size = 16  # Adjust based on your GPU memory
num_batches = (len(data) + batch_size - 1) // batch_size

for i in tqdm(range(num_batches)):
    batch_data = data[i * batch_size: (i + 1) * batch_size]
    batch_texts = [item["patient"] for item in batch_data]
    batch_embeddings = encode_batch(batch_texts)
    
    for j, item in enumerate(batch_data):
        embedding = batch_embeddings[j].tolist()
        client.data_object.create({
            "patient_id": item["patient_id"],
            "patient_uid": item["patient_uid"],
            "PMID": item["PMID"],
            "file_path": item["file_path"],
            "title": item["title"],
            "patient": item["patient"],
            "age": item["age"][0][0],
            "gender": item["gender"],
            "relevant_articles": list(item["relevant_articles"].keys()),
            "similar_patients": list(item["similar_patients"].keys()),
            "embedding": embedding
        }, "MedicalData")