import streamlit as st
import google.generativeai as genai
import json
from PIL import Image

# Configure Gemini
genai.configure(api_key="AIzaSyCNEirXuMFV7GsIyzndWwZLXFvpBx27y2A")

st.title("🍳 DanKitchen - Simple Recipe Extractor")

uploaded_file = st.file_uploader("Upload recipe image", type=["png", "jpg", "jpeg"])

# =========================
# 🔹 FUNCTION TO LIST AVAILABLE MODELS (Run once to debug)
# =========================
def show_available_models():
    """Shows which models are actually available for your API key"""
    st.subheader("🔍 Available Models on Your Account")
    try:
        models = genai.list_models()
        available = []
        for m in models:
            if "generateContent" in m.supported_generation_methods:
                available.append(m.name)
        st.write("✅ These models work:", available[:10])  # Show first 10
        return available
    except Exception as e:
        st.error(f"Could not list models: {e}")
        return []

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    # Show available models first (helps debug)
    available_models = show_available_models()
    
    if st.button("Extract Recipe"):
        # Use CURRENT model names (Gemini 2.5+)
        # Google has deprecated 1.5 models as of March 31, 2026[citation:7]
        current_models = [
            "gemini-2.5-flash",        # Fast, balanced (recommended)
            "gemini-2.5-flash-lite",   # Cheapest, high volume
            "gemini-2.5-pro",          # Best reasoning, slower
            "gemini-3-flash-preview",  # Latest preview
        ]
        
        success = False
        for model_name in current_models:
            try:
                st.write(f"🔄 Trying {model_name}...")
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content([
                    """Extract recipe from this image. Return ONLY valid JSON:
{
  "recipe_name": "",
  "servings": "",
  "ingredients": [{"name": "", "quantity": "", "unit": ""}],
  "steps": [],
  "notes": []
}""",
                    image
                ])
                
                # Parse response
                response_text = response.text
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]
                
                recipe_data = json.loads(response_text.strip())
                
                st.success(f"✅ Success with {model_name}!")
                st.json(recipe_data)
                success = True
                break
                
            except Exception as e:
                st.error(f"❌ {model_name} failed: {e}")
        
        if not success:
            st.error("No working models found. Check available models list above.")