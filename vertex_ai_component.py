import vertexai  
from vertexai.preview.generative_models import GenerativeModel
import json

def notify(text: str, PROJECT_ID):
    vertexai.init(project=PROJECT_ID)
    gemini_pro_model = GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(f"Make markdown notes - with headings, subheadings, points, emojis and descriptive content for the following text : {text}")

    return response.text