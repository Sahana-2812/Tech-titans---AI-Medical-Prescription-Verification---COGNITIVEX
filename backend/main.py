from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input models
class DrugInput(BaseModel):
    drug_name: str
    age: int  # Age in years

class InteractionInput(BaseModel):
    drugs: List[str]

# 1️⃣ Analyze Dosage (age-based)
@app.post("/analyze-dosage")
def analyze_dosage(drug: DrugInput):
    if drug.age < 12:  # child
        dosage_mg = random.choice([25, 50, 75])
    elif drug.age > 65:  # elderly
        dosage_mg = random.choice([50, 75, 100])
    else:  # adult
        dosage_mg = random.choice([100, 150, 200, 250, 300])
    return {"drug": drug.drug_name, "recommended_dosage": f"{dosage_mg}mg", "age": drug.age}

# 2️⃣ Check Interactions (improved)
@app.post("/check-interactions")
def check_interactions(interaction: InteractionInput):
    results = []
    drugs = interaction.drugs
    interactions_db = {
        ("Aspirin", "Ibuprofen"): "May increase bleeding risk",
        ("Paracetamol", "Ibuprofen"): "Generally safe",
        ("Aspirin", "Paracetamol"): "Generally safe",
        ("Metformin", "Cefixime"): "No significant interaction",
        ("Warfarin", "Aspirin"): "High risk of bleeding"
    }
    for i in range(len(drugs)):
        for j in range(i+1, len(drugs)):
            pair = (drugs[i], drugs[j])
            result = interactions_db.get(pair) or interactions_db.get((pair[1], pair[0])) or "No major interactions detected"
            results.append(f"{pair[0]} + {pair[1]}: {result}")
    return {"interactions": results}

# 3️⃣ Suggest Alternatives (age-based)
@app.post("/suggest-alternatives")
def suggest_alternatives(drug: DrugInput):
    alternatives_db = {
        "Aspirin": ["Acetylsalicylic Acid", "Bufferin"],
        "Paracetamol": ["Tylenol", "Panadol"],
        "Ibuprofen": ["Advil", "Motrin"],
        "Metformin": ["Glucophage", "Metformin XR"],
        "Cefixime": ["Suprax", "Cefspan"]
    }
    
    alternatives = alternatives_db.get(drug.drug_name) or [drug.drug_name + "A", drug.drug_name + "B"]
    
    # Child-friendly adjustment
    if drug.age < 12:
        alternatives = [alt for alt in alternatives if "XR" not in alt]
        alternatives = [alt + " (child-friendly)" for alt in alternatives]
    
    return {"alternatives": alternatives, "age": drug.age}


