import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key="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")

# Page config
st.set_page_config(page_title="Adaptive Recipe AI", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.title {
    font-size: 40px;
    font-weight: bold;
    color: #ff6f61;
}
.subtitle {
    font-size: 18px;
    color: #aaa;
}
.box {
    padding: 20px;
    border-radius: 12px;
    background-color: #1c1f26;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">🍲 Adaptive Recipe Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform recipes based on dietary needs using AI</div>', unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Enter Recipe")
    recipe = st.text_area("Paste your recipe here:", height=200)

    st.markdown("### 🥗 Dietary Restrictions")
    diet = st.multiselect(
        "Select restrictions:",
        ["Vegan", "Vegetarian", "Gluten-Free", "Diabetic", "Low-Carb", "High-Protein"]
    )

    generate_btn = st.button("✨ Adapt Recipe")

with col2:
    st.markdown("### 📊 Output")

# Function to call LLM
def generate_recipe(recipe, diet):
    prompt = f"""
You are an expert nutritionist and chef.

Input Recipe:
{recipe}

Dietary Restrictions:
{', '.join(diet)}

Provide:
1. Modified Recipe
2. Nutritional Information
3. Ingredient Substitutions with explanation
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ FIXED MODEL
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# Generate output
if generate_btn:
    if recipe:
        with st.spinner("AI is adapting your recipe... 🍳"):
            result = generate_recipe(recipe, diet)

        with col2:
            st.markdown('<div class="box">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a recipe")

# Footer
st.markdown("---")
st.markdown("💡 Built with Streamlit + Groq (LLaMA 3)")