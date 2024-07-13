#Demo YouTube Link https://youtu.be/rafeuN3tuU4

To set up your medical assistant chatbot environment, follow these steps:

## Setting Up Your Environment

### 1. Installing Python and Virtual Environment

1. **Python Installation:**
   - Ensure Python 3.7 or higher is installed. You can download it from [python.org](https://www.python.org/downloads/) or use a package manager like `apt` (for Linux) or `brew` (for macOS).

2. **Virtual Environment:**
   - It's best to work within a virtual environment to manage dependencies.
   - Install `virtualenv` if you haven't already:
     ```bash
     pip install virtualenv
     ```
   - Create a virtual environment:
     ```bash
     virtualenv medical_assistant_env
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       medical_assistant_env\Scripts\activate
       ```
     - On macOS and Linux:
       ```bash
       source medical_assistant_env/bin/activate
       ```

### 2. Installing Dependencies

1. **Streamlit and Transformers:**
   - These are essential for building the frontend and using the MedCPT model.
   ```bash
   pip install streamlit transformers
   ```

2. **Weaviate:**
   - Install the Weaviate client library for data storage and retrieval.
   ```bash
   pip install weaviate-client
   ```

3. **Ollama and LangChain:**
   - These are used for natural language processing and conversation management.
   ```bash
   pip install ollama langchain
   ```

### 3. Cloning and Organizing Your Project

1. **Clone Your Project:**
   - Clone your project repository or create a new directory for your project.

2. **Organize Files:**
   - Place `app.py` for your Streamlit application and `preprocess_data.py` for data preprocessing in your project directory.

### 4. Running Your Application

1. **Run the Streamlit App:**
   - Navigate to your project directory in the terminal where `app.py` is located.
   - Start the Streamlit server:
     ```bash
     streamlit run app.py
     ```
   - This command launches your medical assistant chatbot application in your default web browser.

### 5. Additional Steps

1. **Configure Weaviate:**
   - Ensure your Weaviate instance is running and accessible. Adjust the Weaviate client URL in `app.py` if needed.

2. **Further Customization:**
   - Customize the chatbot behavior, styling, and integration with external services as per your project requirements.

### 6. External resources and references
   - PMC Data download link https://figshare.com/articles/dataset/PMC-Patients_Dataset/24504115?backTo=/collections/PMC-Patients/6723465

## Conclusion

This setup guide should help you get started with your medical assistant chatbot using Streamlit, Transformers (MedCPT), Weaviate, Ollama, and LangChain. Adjustments may be needed based on your specific project requirements or dependencies.
