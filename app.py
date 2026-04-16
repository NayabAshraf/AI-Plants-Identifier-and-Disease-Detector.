import matplotlib.pyplot as plt
from PIL import Image
import json

from vision_model import identify_plant, detect_disease
from groq_description import generate_plant_and_disease_info

IMAGE_PATH = "images/pest.webp"

def main():
    # Display image
    image = Image.open(IMAGE_PATH)
    plt.imshow(image)
    plt.axis("off")
    plt.show()

    # Step 1: Identify plant
    plant_json = identify_plant(IMAGE_PATH)
    plant_data = json.loads(plant_json)
    
    print("\n🌿 Plant Identification")
    print("----------------------------")
    print(f"Plant Name : {plant_data['plant_name']}")
    print(f"Confidence : {plant_data['confidence']}%")

    # Step 2: Detect disease
    disease_json = detect_disease(IMAGE_PATH)
    disease_data = json.loads(disease_json)
    
    print("\n🦠 Disease Detection")
    print("----------------------------")
    print(f"Disease : {disease_data['disease_label']}")
    print(f"Confidence : {disease_data['confidence']}%")

    # Step 3: Ask user what information they want
    print("\nWhat information would you like to see about the plant?")
    print("Options:")
    print("- category")
    print("- scientific name")
    print("- about")
    print("- temperature")
    print("- sunlight")
    print("- watering")
    print("- repotting")
    print("- fertilizing")
    print("- pests")
    print("- facts")
    print("- care tips")
    if disease_data['disease_label'] != "Healthy":
        print("- disease")  # Show only if disease exists
    print("- full (complete info)")

    user_input = input("\nEnter your choice (comma separated or 'full'): ").strip().lower()

    # Step 4: Generate requested info from Groq
    description = generate_plant_and_disease_info(
        plant_data['plant_name'], 
        disease_data['disease_label'], 
        user_input
    )
    print("\n📘 Plant & Disease Info (Groq LLM)")
    print("--------------------------------------------")
    print(description)


if __name__ == "__main__":
    main()