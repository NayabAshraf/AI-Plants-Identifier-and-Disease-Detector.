import torch
import json
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image

# Step 1: Plant identification
PLANT_MODEL_NAME = "marwaALzaabi/plant-identification-vit"
plant_processor = AutoImageProcessor.from_pretrained(PLANT_MODEL_NAME)
plant_model = AutoModelForImageClassification.from_pretrained(PLANT_MODEL_NAME)
plant_model.eval()

# Step 2: Disease detection
DISEASE_MODEL_NAME = "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
disease_processor = AutoImageProcessor.from_pretrained(DISEASE_MODEL_NAME)
disease_model = AutoModelForImageClassification.from_pretrained(DISEASE_MODEL_NAME)
disease_model.eval()


def identify_plant(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = plant_processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = plant_model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1)
    top_prob, top_class = probs.max(dim=1)

    plant_name = plant_model.config.id2label[top_class.item()]
    confidence = top_prob.item() * 100

    # Return as JSON string
    result = {
        "plant_name": plant_name,
        "confidence": float(f"{confidence:.2f}"),
        "status": "success",
        "model": PLANT_MODEL_NAME
    }
    
    return json.dumps(result)


def detect_disease(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = disease_processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = disease_model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1)
    top_prob, top_class = probs.max(dim=1)

    disease_label = disease_model.config.id2label[top_class.item()]
    confidence = top_prob.item() * 100

    # If the disease label contains "healthy", mark as healthy
    if "healthy" in disease_label.lower():
        disease_label = "Healthy"
        health_status = "healthy"
    else:
        health_status = "diseased"

    # Return as JSON string
    result = {
        "disease_label": disease_label,
        "confidence": float(f"{confidence:.2f}"),
        "health_status": health_status,
        "status": "success",
        "model": DISEASE_MODEL_NAME
    }
    
    return json.dumps(result)