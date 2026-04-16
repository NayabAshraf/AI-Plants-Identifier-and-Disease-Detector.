from groq import Groq
import json

GROQ_API_KEY = "Add your Groq API Key Here..."
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.1-8b-instant"


def generate_plant_and_disease_info(plant_name, disease, user_input):
    # Convert input to list of fields
    requested_fields = [x.strip() for x in user_input.split(",")]
    full_info_requested = "full" in requested_fields

    if disease.lower() == "healthy":
        disease_note = "The plant is healthy. No disease detected."
    else:
        disease_note = f"The plant has the disease: {disease}"

    if full_info_requested:
        prompt = f"""
Provide a comprehensive description of the plant "{plant_name}" and its disease "{disease}" (if any) in simple beginner-friendly language.

Include the following plant details:
- Plant category (e.g., indoor, outdoor, succulent)
- Scientific name
- About (general description)
- Optimal temperature
- Sunlight requirements
- Watering needs
- Repotting frequency and tips
- Fertilizing guidance
- Common pests and how to deal with them
- Interesting plant facts or sayings
- Plant care tips

Then, include detailed information about the disease "{disease}":
1. What the disease is
2. Causes of the disease
3. Symptoms
4. Prevention methods
5. Treatment (both organic and chemical if applicable)

If the plant is healthy, mention "{disease_note}"
"""
    else:
        # Only requested fields
        prompt = f"Provide the following information for the plant '{plant_name}':\n"
        if disease.lower() != "healthy" and "disease" in requested_fields:
            prompt += f"- Disease info for '{disease}' (causes, symptoms, prevention, treatment)\n"

        # Map user requested fields to full descriptions
        field_map = {
            "category": "- Plant category (e.g., indoor, outdoor, succulent)",
            "scientific name": "- Scientific name",
            "about": "- About (general description)",
            "temperature": "- Optimal temperature",
            "sunlight": "- Sunlight requirements",
            "watering": "- Watering needs",
            "repotting": "- Repotting frequency and tips",
            "fertilizing": "- Fertilizing guidance",
            "pests": "- Common pests and how to deal with them",
            "facts": "- Interesting plant facts or sayings",
            "care tips": "- Plant care tips"
        }

        for field in requested_fields:
            if field in field_map:
                prompt += field_map[field] + "\n"

        if disease.lower() == "healthy":
            prompt += f"\nThe plant is healthy. No disease detected.\n"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=1500
    )

    # Return JSON response with the description
    result = {
        "plant_name": plant_name,
        "disease": disease,
        "requested_fields": requested_fields,
        "description": response.choices[0].message.content.strip(),
        "model_used": MODEL_NAME,
        "status": "success"
    }
    
    return json.dumps(result)