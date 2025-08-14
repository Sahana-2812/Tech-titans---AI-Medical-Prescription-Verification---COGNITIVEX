from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input models
class DrugInput(BaseModel):
    drug_name: str

class InteractionInput(BaseModel):
    drugs: List[str]

# 1️⃣ Analyze Dosage (dynamic)
@app.post("/analyze-dosage")
def analyze_dosage(drug: DrugInput):
    # Generate a random realistic dosage between 50mg and 500mg
    dosage_mg = random.choice([50, 75, 100, 150, 200, 250, 300, 400, 500])
    return {"drug": drug.drug_name, "recommended_dosage": f"{dosage_mg}mg"}

# 2️⃣ Check Interactions (simulated)
@app.post("/check-interactions")
def check_interactions(interaction: InteractionInput):
    results = []
    drugs = interaction.drugs
    
    # Sample known interactions
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
            # Check both orders in db
            result = interactions_db.get(pair) or interactions_db.get((pair[1], pair[0])) or "No major interactions detected"
            results.append(f"{pair[0]} + {pair[1]}: {result}")
    
    return {"interactions": results}

# 3️⃣ Suggest Alternatives (simulated)
@app.post("/suggest-alternatives")
def suggest_alternatives(drug: DrugInput):
    # Known alternatives database
    alternatives_db = {
        "Aspirin": ["Acetylsalicylic Acid", "Bufferin"],
        "Paracetamol": ["Tylenol", "Panadol"],
        "Ibuprofen": ["Advil", "Motrin"],
        "Metformin": ["Glucophage", "Metformin XR"],
        "Cefixime": ["Suprax", "Cefspan"]
    }
    
    # Get alternatives if available, else generate two simulated options
    alternatives = alternatives_db.get(drug.drug_name) or [drug.drug_name + "A", drug.drug_name + "B"]
    
    return {"alternatives": alternatives}

