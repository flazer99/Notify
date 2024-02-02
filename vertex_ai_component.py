import vertexai  
from vertexai.preview.generative_models import GenerativeModel
import json

def notify(text: str, PROJECT_ID):
    vertexai.init(project=PROJECT_ID)
    gemini_pro_model = GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(f"""Create markdown notes that include headings, subheadings, bullet points, emojis, and descriptive content for the following text. 
    Additionally, incorporate any relevant information in a separate section as you deem necessary : {text}""")

    return response.text