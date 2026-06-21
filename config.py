import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
DATABASE_PATH = os.path.join(BASE_DIR, "dental.db")
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
DOWNLOADS_DIR = "/tmp"

# ضع مفتاح API الخاص بك هنا
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6IQbGoETFwRQuMgx3pWzmlwPr0GcBqtHW3ZGTkeGr55Mg")
GEMINI_MODEL = "gemini-2.0-flash"

ARIAL_FONT_PATH = os.path.join(BASE_DIR, "Arial.ttf")
CLINIC_LOGO_PATH = os.path.join(BASE_DIR, "clinic_logo.png")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_doctor():
    s = load_settings()
    return {
        "name": s.get("name", "Dr. Hothaifa Al-Hamdani"),
        "phone": s.get("phone", "+967 777 777 777"),
        "specialty": s.get("specialty", "Oral & Dental Surgery"),
        "license": s.get("license", "License: 12345"),
        "clinic": s.get("clinic", "Dental Hothaifa Clinic")
    }

DRUG_CATEGORIES = [
    "Antibiotic", "Analgesic", "Antifungal", "Antiviral",
    "Hemostatic", "Emergency", "Mouth Preparation", "Tooth Paste",
    "Gel", "Muscle Relaxant", "Vitamin", "Anti-edematous", "Sedative"
]
