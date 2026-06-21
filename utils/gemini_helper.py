import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

def analyze_case(symptoms, age, gender, chronic, allergies):
    prompt = f"""As a dental specialist, analyze:
Symptoms: {symptoms}
Age: {age}, Gender: {gender}
Chronic: {chronic or 'none'}, Allergies: {allergies or 'none'}
Provide: 1. Differential diagnoses 2. Most likely diagnosis 3. Recommended medications (generic names) 4. Precautions"""
    try:
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return f"AI Error: {e}"
