import streamlit as st
import pytesseract
from PIL import Image
import re
import google.generativeai as genai
import json

genai.configure(api_key="your_api_key_here")
# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🧑‍🍳 App Branding
st.title("🍳 DanKitchen - AI Recipe Extractor")
st.subheader("Built from Danny’s idea ✨")

uploaded_file = st.file_uploader("Upload a recipe image", type=["png", "jpg", "jpeg"])

# =========================
# 🔹 CLEAN OCR TEXT (FIXED)
# =========================
def clean_text(text):
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()

        # remove junk lines
        if len(line) < 3:
            continue
        if not any(c.isalpha() for c in line):
            continue

        cleaned.append(line)

    return cleaned


# =========================
# 🔹 BASIC PARSER
# =========================
def parse_recipe_fallback(text):
    lines = text.split("\n")

    ingredients = []
    quantities = []
    notes = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        qty = re.findall(r"\d+\s*(tbsp|tsp|cup|cups|g|ml|kg|pcs|piece)?", line.lower())

        if qty:
            quantities.append(qty[0])
            ingredients.append(line)
            notes.append("Ingredient detected")
        else:
            ingredients.append(line)
            quantities.append("N/A")
            notes.append("Step / note")

    return ingredients, quantities, notes


# =========================
# 🔹 AI PARSER (placeholder)
# =========================


def parse_with_ai(text):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
Extract recipe data from this text.

Return ONLY JSON:
{{
  "ingredients": [
    {{"name": "", "quantity": "", "unit": ""}}
  ],
  "steps": [],
  "cook_time": ""
}}

TEXT:
{text}
"""

    response = model.generate_content(prompt)

    try:
        data = json.loads(response.text)
    except:
        data = {"ingredients": [], "steps": [], "cook_time": ""}

    ingredients = [f"{i['name']} ({i['quantity']} {i['unit']})" for i in data.get("ingredients", [])]
    quantities = [i["quantity"] for i in data.get("ingredients", [])]
    notes = data.get("steps", [])

    return ingredients, quantities, notes
    prompt_output = {
        "ingredients": [],
        "quantities": [],
        "notes": []
    }

    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if any(word in line.lower() for word in ["cup", "tbsp", "tsp", "clove", "ml", "gram"]):
            prompt_output["ingredients"].append(line)
            prompt_output["quantities"].append("auto-detected")
            prompt_output["notes"].append("AI classified ingredient")
        else:
            prompt_output["ingredients"].append(line)
            prompt_output["quantities"].append("N/A")
            prompt_output["notes"].append("AI classified step")

    return (
        prompt_output["ingredients"],
        prompt_output["quantities"],
        prompt_output["notes"]
    )


# =========================
# 🔹 UI
# =========================
use_ai = st.toggle("🧠 Use AI Mode (simulated now)")

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Recipe", width="stretch")

    # OCR
    raw_text = pytesseract.image_to_string(image)

    cleaned_lines = clean_text(raw_text)
    text = "\n".join(cleaned_lines)

    st.subheader("📄 Raw Extracted Text")
    st.write(text)

    # 🔽 NEW: Show captured text line by line
    st.subheader("🔍 Captured Text (Line by Line)")
    if cleaned_lines:
        for idx, line in enumerate(cleaned_lines, start=1):
            st.write(f"{idx}. {line}")
    else:
        st.write("⚠️ No text detected from image.")

    # Mode selection
    if use_ai:
        st.info("AI mode enabled (placeholder logic running)")
        ingredients, quantities, notes = parse_with_ai(text)
    else:
        st.info("Using basic parser")
        ingredients, quantities, notes = parse_recipe_fallback(text)

    st.subheader("📊 Structured Recipe Table")

    st.table({
        "Ingredient / Step": ingredients,
        "Quantity": quantities,
        "Notes": notes
    })