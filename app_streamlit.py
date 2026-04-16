import streamlit as st
from PIL import Image
import io
import matplotlib.pyplot as plt
import sys
import os
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import existing logic
from vision_model import identify_plant, detect_disease
from groq_description import generate_plant_and_disease_info
from plant_image_fetcher import get_plant_images   # ✅ NEW

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Plant Doctor 🌱",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Styling
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4efe9 100%);
}

.main-header {
    background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.result-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
    border-top: 5px solid #4CAF50;
}

.healthy {
    background: #e8f5e9;
    padding: 1rem;
    border-radius: 10px;
    color: #1b5e20;
    font-weight: bold;
}

.diseased {
    background: #ffebee;
    padding: 1rem;
    border-radius: 10px;
    color: #b71c1c;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## 🌿 Plant Doctor")
    st.markdown("AI-powered plant identification & disease detection")

    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. Upload a plant image  
    2. Click **Analyze Plant**  
    3. Select info you want  
    4. View results & related images  
    """)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🌱 Plant Doctor</h1>
    <p>Upload a plant image to identify and diagnose it</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Layout
# -------------------------------------------------
col1, col2 = st.columns([1, 1])

# =================================================
# LEFT COLUMN — Upload + Analyze
# =================================================
with col1:
    st.markdown("### 📤 Upload Plant Image")

    uploaded_file = st.file_uploader(
        "Choose a plant image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        image_path = "temp_uploaded_image.jpg"
        image.save(image_path)

        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("🔍 Analyze Plant", use_container_width=True):
            with st.spinner("Analyzing plant..."):
                try:
                    plant_json = identify_plant(image_path)
                    disease_json = detect_disease(image_path)

                    plant_data = json.loads(plant_json)
                    disease_data = json.loads(disease_json)

                    st.session_state["plant_name"] = plant_data["plant_name"]
                    st.session_state["plant_conf"] = plant_data["confidence"]

                    st.session_state["disease_label"] = disease_data["disease_label"]
                    st.session_state["disease_conf"] = disease_data["confidence"]
                    st.session_state["health_status"] = disease_data["health_status"]

                    st.session_state["plant_data"] = plant_data
                    st.session_state["disease_data"] = disease_data

                except Exception as e:
                    st.error(f"Error: {e}")

# =================================================
# RIGHT COLUMN — Results
# =================================================
with col2:
    if "plant_name" in st.session_state:

        st.markdown("### 📊 Analysis Results")

        # ---------------- PLANT INFO ----------------
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown("### 🌿 Plant Identification")

        st.markdown(f"**Plant Name:** {st.session_state['plant_name']}")
        st.markdown(f"**Confidence:** {st.session_state['plant_conf']:.2f}%")

        with st.expander("View JSON"):
            st.json(st.session_state["plant_data"])

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- DISEASE INFO ----------------
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown("### 🦠 Disease Detection")

        if st.session_state["health_status"] == "healthy":
            st.markdown(f"<div class='healthy'>✅ Healthy Plant</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div class='diseased'>⚠️ Disease Detected: {st.session_state['disease_label']}</div>",
                unsafe_allow_html=True
            )

        st.markdown(f"**Confidence:** {st.session_state['disease_conf']:.2f}%")

        with st.expander("View JSON"):
            st.json(st.session_state["disease_data"])

        st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# INFORMATION + RELATED IMAGES
# =================================================
if "plant_name" in st.session_state:

    st.markdown("---")
    st.markdown("## 📚 Get Plant Information")

    info_options = [
        "category", "scientific name", "about", "temperature",
        "sunlight", "watering", "repotting",
        "fertilizing", "pests", "facts", "care tips"
    ]

    if st.session_state["disease_label"].lower() != "healthy":
        info_options.append("disease")

    info_options.append("full")
    info_options.append("related images")  # ✅ NEW

    selected_options = []
    show_related_images = False

    cols = st.columns(3)
    for i, option in enumerate(info_options):
        with cols[i % 3]:
            if option == "related images":
                if st.checkbox("Related Images"):
                    show_related_images = True
            else:
                if st.checkbox(option.replace("_", " ").title(), key=f"opt_{option}"):
                    selected_options.append(option)

    # ---------------------------------------------
    # Generate text info
    # ---------------------------------------------
    if selected_options:
        user_input = ",".join(selected_options)

        if st.button("📖 Generate Plant Information", use_container_width=True):
            with st.spinner("Generating information..."):
                try:
                    response_json = generate_plant_and_disease_info(
                        st.session_state["plant_name"],
                        st.session_state["disease_label"],
                        user_input
                    )

                    data = json.loads(response_json)

                    st.markdown("### 📘 Plant & Disease Information")
                    st.markdown(data["description"])

                    with st.expander("View JSON"):
                        st.json(data)

                except Exception as e:
                    st.error(str(e))

    # ---------------------------------------------
    # SHOW RELATED IMAGES (DuckDuckGo)
    # ---------------------------------------------
    if show_related_images:
        st.markdown("---")
        st.markdown("## 🖼️ Related Plant Images")

        with st.spinner("Fetching images..."):
            try:
                image_paths = get_plant_images(st.session_state["plant_name"])

                if image_paths:
                    cols = st.columns(len(image_paths))
                    for i, img_path in enumerate(image_paths):
                        if os.path.exists(img_path):
                            with cols[i]:
                                st.image(img_path, use_column_width=True)
                else:
                    st.info("No images found.")

            except Exception as e:
                st.error(f"Image fetch failed: {e}")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align:center; color: #666;">
🌱 <b>Plant Doctor</b> — AI-powered Plant Identification & Disease Detection  
</div>
""", unsafe_allow_html=True)
