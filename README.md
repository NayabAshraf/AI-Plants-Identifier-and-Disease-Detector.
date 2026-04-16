🌱 Plant Doctor — AI-Powered Plant Identification & Disease Detection

Plant Doctor is an AI-based web application that identifies plants from
images and detects diseases using deep learning models. It also provides
detailed plant care information and related images.


 FEATURES:
 
-   Plant Identification using Vision Transformer (ViT)
-   Disease Detection using MobileNetV2
-   AI-generated Plant Information (Groq LLM)
-   Related Plant Images Fetching (DuckDuckGo)
-   Confidence Scores for predictions
-   Interactive Streamlit UI
-   JSON Output View for Debugging

TECH STACK:

Frontend: Streamlit

Backend: Python

AI Models: Hugging Face Transformers

LLM: Groq (LLaMA 3.1)

Image Search: DuckDuckGo

Libraries: - torch - transformers - streamlit - pillow - matplotlib -
duckduckgo-search - requests


PROJECT STRUCTURE:

plant-doctor/

app_streamlit.py # Streamlit Web App

app.py # CLI Version

vision_model.py # AI Models

groq_description.py # LLM Info Generator

plant_image_fetcher.py # Image Fetching


INSTALLATION:

1.  Clone Repo:

2.  git clone https://github.com/NayabAshraf/AI-Plants-Identifier-and-Disease-Detector.
    
    cd plant-doctor
    
3.  Create Virtual Environment: python -m venv venv
  
4.  Install Dependencies: pip install -r requirements.txt

SETUP:

Add your Groq API key in: groq_description.py

GROQ_API_KEY = “your_api_key_here”

RUN APP:

Streamlit: streamlit run app_streamlit.py

Open in browser: http://localhost:8501

CLI: python app.py

HOW IT WORKS:
1.  Upload image
2.  Identify plant
3.  Detect disease
4.  Show confidence
5.  Generate info
6.  Fetch images

MODELS USED:

Plant Model: marwaALzaabi/plant-identification-vit

Disease Model: linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification

