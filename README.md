# 🍳 DanKitchen - AI Recipe Extractor

This project extracts recipes from images using Google Gemini AI. Upload any recipe photo or screenshot, and the AI automatically extracts ingredients with quantities and units into a structured table.

## Prerequisites

- Python 3.8+
- Install dependencies:

    pip install streamlit google-generativeai pillow pandas python-dotenv

- Configure environment variables (get your free API key from Google AI Studio):

    # For Windows CMD
    set GOOGLE_API_KEY=your_api_key_here

    # For Windows PowerShell
    $env:GOOGLE_API_KEY="your_api_key_here"

    # For Mac/Linux
    export GOOGLE_API_KEY=your_api_key_here

## Executable Files and Commands

Run all commands from the project root folder (the folder containing app.py).

### 1) Run the Recipe Extractor App

File: app.py

Purpose:
- Launches the Streamlit web interface
- Allows users to upload recipe images (PNG, JPG, JPEG)
- Uses Google Gemini AI to extract recipe information
- Displays ingredients in a structured table format

Command:

    streamlit run app.py

Optional arguments:

    streamlit run app.py --server.port 8501 --server.address localhost

### 2) Test with Different Gemini Models

File: app.py (model selection dropdown)

Purpose:
- Switch between different Gemini models for comparison
- Available models: gemini-2.5-flash (fastest), gemini-2.5-pro (most accurate), gemini-2.0-flash (legacy)

How to use:
- Select model from dropdown in the app interface
- Click "Extract Recipe" button

### 3) Quick Test Script (Optional)

File: test_gemini.py (create this file for testing)

Purpose:
- Verifies API key is working
- Lists all available models for your account
- Tests basic API connectivity

Command:

    python test_gemini.py

## Recommended End-to-End Order

1. Set up your Google Gemini API key:

    # Get free API key from https://aistudio.google.com/
    set GOOGLE_API_KEY=your_api_key_here

2. Install dependencies:

    pip install -r requirements.txt

3. Run the app:

    streamlit run app.py

4. Upload a recipe image (use flexible-recipe-formatting.png as test)

5. Select model (recommended: gemini-2.5-flash)

6. Click "Extract Recipe"

7. View the structured ingredients table

## Outputs

- Streamlit web interface (opens in browser automatically)
- Ingredients table with columns:
  - 🥕 Ingredient (name of ingredient)
  - 📊 Quantity (number or fraction)
  - 📏 Unit (tbsp, tsp, cup, g, ml, kg, piece, etc.)
- Raw JSON response (expandable section for debugging)
- Recipe name and serving size (if detected)

## Sample Results (Deviled Eggs Recipe)

Input Image Text:

Deviled Eggs Servings 12
Ingredients
6 Hard Boiled Eggs
1/3 C. Mayonnaise
1 tsp Dill Pickle Relish, drained
Sriracha Sauce, pea size dollop
Dash of Garlic Powder
Dash of Salt
Dash of Pepper
Paprika


Output Table:

| 🥕 Ingredient | 📊 Quantity | 📏 Unit |
|---------------|-------------|---------|
| Hard Boiled Eggs | 6 | pieces |
| Mayonnaise | 1/3 | cup |
| Dill Pickle Relish | 1 | tsp |
| Sriracha Sauce | pea size dollop | - |
| Garlic Powder | dash | - |
| Salt | dash | - |
| Pepper | dash | - |
| Paprika | - | - |

## Sample Results (Avgolemono Soup Recipe)

Input Image Text:

Avgolemono Soup
Ingredients:
1 tbsp olive oil
1 onion, diced
3 cloves garlic, minced
8-10 cups chicken broth
1 cup whole wheat orzo pasta
3 cups cooked chicken (shredded)
3 eggs
1/2 cup lemon juice
1 handful fresh spinach
1 1/2 tsp salt
Freshly ground pepper to taste
Fresh dill to taste


Output Table:

| 🥕 Ingredient | 📊 Quantity | 📏 Unit |
|---------------|-------------|---------|
| olive oil | 1 | tablespoon |
| onion, diced | 1 | - |
| garlic, minced | 3 | cloves |
| chicken broth | 8-10 | cups |
| whole wheat orzo | 1 | cup |
| cooked chicken | 3 | cups |
| eggs | 3 | - |
| lemon juice | 1/2 | cup |
| fresh spinach | 1 | handful |
| salt | 1 1/2 | teaspoons |
| freshly ground pepper | to taste | - |
| fresh dill | to taste | - |

