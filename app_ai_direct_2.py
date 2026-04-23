import streamlit as st
import google.generativeai as genai
import json
from PIL import Image
import pandas as pd

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

# =========================
# 🔹 FUNCTION TO DISPLAY INGREDIENTS TABLE
# =========================
def display_ingredients_table(recipe_data):
    """Create a beautiful table from ingredients data"""
    
    ingredients = recipe_data.get("ingredients", [])
    
    if not ingredients:
        st.warning("No ingredients found in the recipe")
        return
    
    # Convert to DataFrame for better table display
    df = pd.DataFrame(ingredients)
    
    # Rename columns for better display
    df = df.rename(columns={
        "name": "🥕 Ingredient",
        "quantity": "📊 Quantity",
        "unit": "📏 Unit"
    })
    
    # Fill empty units with "-"
    df["📏 Unit"] = df["📏 Unit"].fillna("-")
    df["📏 Unit"] = df["📏 Unit"].replace("", "-")
    
    # Display recipe metadata if available
    col1, col2 = st.columns(2)
    with col1:
        if recipe_data.get("recipe_name"):
            st.info(f"📖 **Recipe:** {recipe_data['recipe_name']}")
    with col2:
        if recipe_data.get("servings"):
            st.info(f"👥 **Servings:** {recipe_data['servings']}")
    
    # Display the table
    st.subheader("🥗 Ingredients List")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "🥕 Ingredient": st.column_config.TextColumn("🥕 Ingredient", width="large"),
            "📊 Quantity": st.column_config.TextColumn("📊 Quantity", width="medium"),
            "📏 Unit": st.column_config.TextColumn("📏 Unit", width="small"),
        }
    )
    
    # Alternative: Simple table using st.table (if you prefer)
    # st.table(df)
    
    # Display steps if available
    steps = recipe_data.get("steps", [])
    if steps:
        st.subheader("📝 Instructions")
        for idx, step in enumerate(steps, 1):
            st.write(f"{idx}. {step}")
    
    # Display notes if available
    notes = recipe_data.get("notes", [])
    if notes:
        st.subheader("📌 Notes")
        for note in notes:
            st.write(f"• {note}")

# =========================
# 🔹 FUNCTION TO EXTRACT RECIPE
# =========================
def extract_recipe_from_image(image, model_name):
    """Extract recipe from image using specified model"""
    
    model = genai.GenerativeModel(model_name)
    
    # Enhanced prompt for better extraction
    prompt = """Extract recipe from this image. Return ONLY valid JSON with NO additional text:

{
  "recipe_name": "",
  "servings": "",
  "ingredients": [
    {"name": "ingredient name", "quantity": "number or fraction", "unit": "tbsp, tsp, cup, g, ml, kg, piece, etc."}
  ],
  "steps": [],
  "notes": []
}

IMPORTANT RULES:
- For quantity, keep as number or fraction (e.g., "1", "1/2", "2", "3")
- For unit, use standard abbreviations (tbsp, tsp, cup, g, ml, kg, piece, clove, handful, dash)
- If no specific unit, leave as empty string
- Extract ALL ingredients from the image
- If you see cooking steps/instructions, put them in the steps array
- If you see notes like "refrigerate", "boil", "freeze", put them in notes array
"""
    
    response = model.generate_content([prompt, image])
    
    # Parse response
    response_text = response.text
    
    # Clean markdown code blocks
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]
    
    # Remove any trailing commas or invalid JSON
    response_text = response_text.strip()
    
    try:
        recipe_data = json.loads(response_text)
        return recipe_data
    except json.JSONDecodeError as e:
        st.error(f"JSON parsing error: {e}")
        st.text("Raw response:", response_text)
        return None

# =========================
# 🔹 MAIN UI
# =========================
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    # Show available models first (helps debug)
    available_models = show_available_models()
    
    # Model selection dropdown
    model_choice = st.selectbox(
        "🤖 Choose AI Model:",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"],
        help="Select which Gemini model to use for extraction"
    )
    
    if st.button("🔍 Extract Recipe", type="primary"):
        with st.spinner(f"🔄 Analyzing image with {model_choice}..."):
            recipe_data = extract_recipe_from_image(image, model_choice)
        
        if recipe_data:
            st.success("✅ Recipe extracted successfully!")
            
            # Show raw JSON in expander (for debugging)
            with st.expander("📄 View Raw JSON Response"):
                st.json(recipe_data)
            
            # Display ingredients table
            display_ingredients_table(recipe_data)
        else:
            st.error("❌ Failed to extract recipe. Please try again with a clearer image.")

# =========================
# 🔹 SIDEBAR WITH INFO
# =========================
with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. **Upload** a recipe image (PNG, JPG, JPEG)
    2. **Select** the AI model (gemini-2.5-flash is fastest)
    3. **Click** Extract Recipe
    4. **View** the structured ingredients table
    
    ### 📋 Features
    - ✅ Automatically extracts ingredients
    - ✅ Shows quantities and units
    - ✅ No manual typing needed
    - ✅ Works with photos and screenshots
    
    ### 🎯 Tips for Best Results
    - Use clear, well-lit images
    - Crop out unnecessary background
    - Make sure text is readable
    """)
    
    st.divider()
    
    st.header("📊 Example Output")
    st.markdown("""
    | Ingredient | Quantity | Unit |
    |------------|----------|------|
    | olive oil | 1 | tablespoon |
    | onion, diced | 1 | - |
    | garlic, minced | 3 | cloves |
    | chicken broth | 8-10 | cups |
    | cooked chicken | 3 | cups |
    """)