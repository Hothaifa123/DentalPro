import google.generativeai as genai
import os

API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6IQbGoETFwRQuMgx3pWzmlwPr0GcBqtHW3ZGTkeGr55Mg")
MODEL_NAME = "gemini-2.0-flash"

def analyze_case(symptoms, age, gender, chronic, allergies):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""As a dental specialist, analyze:
Symptoms: {symptoms}
Age: {age}, Gender: {gender}
Chronic: {chronic or 'none'}, Allergies: {allergies or 'none'}
Provide: 1. Differential diagnoses 2. Most likely diagnosis 3. Recommended medications 4. Precautions"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}. Check API key in Render Environment Variables."
