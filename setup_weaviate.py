import weaviate
import json

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")  # Update URL if using Weaviate Cloud

# Define the schema for the MedicalData class
schema = {
    "classes": [
        {
            "class": "MedicalData",
            "description": "Medical data for patients with various conditions",
            "properties": [
                {"name": "patient_id", "dataType": ["string"]},
                {"name": "patient_uid", "dataType": ["string"]},
                {"name": "PMID", "dataType": ["string"]},
                {"name": "file_path", "dataType": ["string"]},
                {"name": "title", "dataType": ["text"]},
                {"name": "patient", "dataType": ["text"]},
                {"name": "age", "dataType": ["number[]"]},
                {"name": "gender", "dataType": ["string"]},
                {"name": "relevant_articles", "dataType": ["int[]"]},
                {"name": "similar_patients", "dataType": ["int[]"]},
                {"name": "embedding", "dataType": ["number[]"]}
            ]
        }
    ]
}

# Create schema in Weaviate
client.schema.create(schema)

# Load the encoded data
with open('encoded_data.json') as f:
    encoded_data = json.load(f)

# Import data into Weaviate
for item in encoded_data:
    client.data_object.create(
        {
            "patient_id": item["patient_id"],
            "patient_uid": item["patient_uid"],
            "PMID": item["PMID"],
            "file_path": item["file_path"],
            "title": item["title"],
            "patient": item["patient"],
            "age": item["age"],
            "gender": item["gender"],
            "relevant_articles": item["relevant_articles"],
            "similar_patients": item["similar_patients"],
            "embedding": item["embedding"]
        },
        class_name="MedicalData"
    )