# ml_model.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Mock dataset for symptoms and diseases
data = [
    {"symptoms": ["cough", "fever"], "disease": "Flu"},
    {"symptoms": ["sore throat", "cough"], "disease": "Cold"},
    {"symptoms": ["fatigue", "shortness of breath"], "disease": "Asthma"},
    {"symptoms": ["headache", "nausea"], "disease": "Migraine"},
    {"symptoms": ["persistent cough", "weight loss"], "disease": "Tuberculosis"},
    {"symptoms": ["muscle pain", "fever"], "disease": "Influenza"},
    {"symptoms": ["dry mouth", "thirst"], "disease": "Dehydration"},
    {"symptoms": ["anxiety", "fatigue"], "disease": "Chronic Stress"},
    {"symptoms": ["blurred vision", "eye pain"], "disease": "Glaucoma"},
    {"symptoms": ["shortness of breath", "fatigue"], "disease": "Heart Failure"},
    {"symptoms": ["itchy skin", "rash"], "disease": "Eczema"},
    {"symptoms": ["sneezing", "runny nose"], "disease": "Common Cold"},
    {"symptoms": ["difficulty concentrating", "restlessness"], "disease": "Attention Deficit Disorder"},
    {"symptoms": ["sweating", "tremors"], "disease": "Hypoglycemia"},
    {"symptoms": ["weight gain", "fatigue"], "disease": "Hypothyroidism"},
    {"symptoms": ["joint pain", "stiffness"], "disease": "Arthritis"},
    {"symptoms": ["burning sensation", "frequent urination"], "disease": "Urinary Tract Infection"},
    {"symptoms": ["dry cough", "fatigue"], "disease": "Bronchitis"},
    {"symptoms": ["irritability", "difficulty sleeping"], "disease": "Insomnia"},
    {"symptoms": ["nausea", "vomiting"], "disease": "Gastroenteritis"},
    {"symptoms": ["fever", "body aches"], "disease": "Viral Fever"},
    {"symptoms": ["dizziness", "fatigue"], "disease": "Anemia"},
    {"symptoms": ["hair loss", "brittle nails"], "disease": "Iron Deficiency"},
    {"symptoms": ["sensitivity to light", "eye pain"], "disease": "Photophobia"},
    {"symptoms": ["numbness", "tingling"], "disease": "Peripheral Neuropathy"},
    {"symptoms": ["stomach cramps", "diarrhea"], "disease": "Food Poisoning"},
    {"symptoms": ["abdominal pain", "bloating"], "disease": "Irritable Bowel Syndrome"},
    {"symptoms": ["sore throat", "difficulty swallowing"], "disease": "Strep Throat"},
    {"symptoms": ["chest pain", "sweating"], "disease": "Panic Attack"},
    {"symptoms": ["persistent itching", "dry skin"], "disease": "Psoriasis"},
    {"symptoms": ["difficulty breathing", "swelling"], "disease": "Anaphylaxis"},
    {"symptoms": ["frequent headaches", "neck stiffness"], "disease": "Tension Headache"},
    {"symptoms": ["fever", "chills"], "disease": "Malaria"},
    {"symptoms": ["fatigue", "loss of appetite"], "disease": "Mononucleosis"},
    {"symptoms": ["numbness in hands", "stiff neck"], "disease": "Cervical Spondylosis"},
    {"symptoms": ["hearing loss", "ear pain"], "disease": "Ear Infection"},
    {"symptoms": ["frequent urination", "thirst"], "disease": "Diabetes"},
    {"symptoms": ["heartburn", "chest discomfort"], "disease": "Acid Reflux"},
    {"symptoms": ["shoulder pain", "arm weakness"], "disease": "Rotator Cuff Injury"},
    {"symptoms": ["coughing", "sore throat"], "disease": "Tonsillitis"},
    {"symptoms": ["nasal congestion", "loss of smell"], "disease": "Sinus Infection"},
    {"symptoms": ["itchy scalp", "dandruff"], "disease": "Seborrheic Dermatitis"},
    {"symptoms": ["knee pain", "swelling"], "disease": "Meniscus Tear"},
    {"symptoms": ["blurred vision", "eye redness"], "disease": "Conjunctivitis"},
    {"symptoms": ["skin rash", "fever"], "disease": "Chickenpox"},
    {"symptoms": ["back pain", "muscle stiffness"], "disease": "Sciatica"},
    {"symptoms": ["hoarseness", "throat pain"], "disease": "Laryngitis"},
    {"symptoms": ["fever", "sweats"], "disease": "Endocarditis"},
    {"symptoms": ["difficulty urinating", "pelvic pain"], "disease": "Prostatitis"},
    {"symptoms": ["loss of balance", "dizziness"], "disease": "Vertigo"},
    {"symptoms": ["mouth sores", "bleeding gums"], "disease": "Oral Thrush"},
    {"symptoms": ["muscle weakness", "fatigue"], "disease": "Fibromyalgia"},
    {"symptoms": ["pain in leg", "swelling"], "disease": "Deep Vein Thrombosis"},
    {"symptoms": ["burning sensation", "foot pain"], "disease": "Plantar Fasciitis"},
    {"symptoms": ["persistent sadness", "loss of interest", "insomnia"], "disease": "Depression"},
    {"symptoms": ["mood swings", "increased energy", "impulsivity"], "disease": "Bipolar Disorder"},
    {"symptoms": ["chest pain", "shortness of breath", "coughing up blood"], "disease": "Pulmonary Embolism"},
    {"symptoms": ["runny nose", "sneezing", "nasal congestion"], "disease": "Allergic Rhinitis"},
    {"symptoms": ["toothache", "swollen gums", "bad breath"], "disease": "Gingivitis"},
    {"symptoms": ["difficulty breathing", "wheezing", "chronic cough"], "disease": "Chronic Obstructive Pulmonary Disease (COPD)"},
    {"symptoms": ["fever", "cough", "shortness of breath", "chest pain"], "disease": "Pneumonia"},
    {"symptoms": ["loss of appetite", "low energy", "sleep problems"], "disease": "Anxiety"},
    {"symptoms": ["dry mouth", "tooth decay", "bad breath"], "disease": "Dry Mouth Syndrome"},
    {"symptoms": ["runny nose", "itchy eyes", "sneezing"], "disease": "Seasonal Allergies"},
    {"symptoms": ["wheezing", "shortness of breath", "chest tightness"], "disease": "Bronchitis"},
    {"symptoms": ["insomnia", "constant worrying", "restlessness"], "disease": "Generalized Anxiety Disorder"},
    {"symptoms": ["headache", "blurred vision", "light sensitivity"], "disease": "Migraine"},
    {"symptoms": ["swelling around the nose", "runny nose", "pain in the face"], "disease": "Sinusitis"},
    {"symptoms": ["trembling", "fast heartbeat", "fear of losing control"], "disease": "Panic Disorder"},
    {"symptoms": ["chronic cough", "phlegm production", "shortness of breath"], "disease": "Emphysema"},
    # Add more examples as necessary
]

# Encode symptoms and diseases for the model
all_symptoms = list(set(s for entry in data for s in entry["symptoms"]))
all_diseases = list(set(entry["disease"] for entry in data))

symptom_encoder = LabelEncoder().fit(all_symptoms)
disease_encoder = LabelEncoder().fit(all_diseases)

X = np.array([np.isin(all_symptoms, entry["symptoms"]).astype(int) for entry in data])
y = disease_encoder.transform([entry["disease"] for entry in data])

# Split and train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

def predict_disease(symptoms):
    symptom_vector = np.isin(all_symptoms, symptoms).astype(int).reshape(1, -1)
    prediction = model.predict(symptom_vector)
    disease = disease_encoder.inverse_transform(prediction)[0]
    return disease
