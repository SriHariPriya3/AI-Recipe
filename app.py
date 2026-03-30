import streamlit as st
from groq import Groq
import os
import pandas as pd
import ast
import matplotlib.pyplot as plt
import plotly.express as px
from dotenv import load_dotenv

# -----------------------------
# Load API key
# -----------------------------
load_dotenv()

client = Groq(api_key=os.getenv("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"))

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Adaptive Recipe Intelligence",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.title {
font-size:40px;
font-weight:bold;
color:#ff6f61;
}

.subtitle {
font-size:18px;
color:#aaa;
}

.box {
padding:20px;
border-radius:12px;
background-color:#1c1f26;
box-shadow:0px 4px 10px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_dataset():
    df = pd.read_csv("RAW_recipes.csv")
    df = df[["name","ingredients","steps","minutes"]].head(500)
    return df

df = load_dataset()

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Adaptive Recipe Intelligence")

menu = st.sidebar.radio(
"Navigation",
["Home","Recipe Adapter","Nutrition Insights","Report & Reviews","Visualizations"]
)

# -----------------------------
# HOME TAB
# -----------------------------
if menu == "Home":

    st.markdown('<div class="title">🍲 Adaptive Recipe Intelligence</div>', unsafe_allow_html=True)

    st.markdown('<div class="subtitle">Transform recipes based on dietary needs using AI</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("""
### Project Overview

Adaptive Recipe Intelligence uses **Generative AI** to modify recipes based on dietary needs.

### Features

- AI recipe adaptation
- Ingredient substitutions
- Nutritional analysis
- Interactive visualizations
- Dataset recipe selection

### Technologies

- Streamlit
- Groq LLaMA
- Pandas
- Plotly
- Matplotlib
""")

# -----------------------------
# RECIPE ADAPTER TAB
# -----------------------------
elif menu == "Recipe Adapter":

    col1, col2 = st.columns([1,1])

    with col1:

        st.subheader("📚 Choose Recipe From Dataset")

        recipe_list = df["name"].dropna().tolist()

        selected_recipe = st.selectbox(
        "Select recipe",
        ["None"] + recipe_list
        )

        dataset_recipe = ""

        if selected_recipe != "None":

            recipe_row = df[df["name"] == selected_recipe].iloc[0]

            ingredients = ast.literal_eval(recipe_row["ingredients"])
            steps = ast.literal_eval(recipe_row["steps"])

            ingredient_text = "\n".join(ingredients)
            steps_text = "\n".join(steps)

            dataset_recipe = f"""
Recipe: {recipe_row['name']}

Cooking Time: {recipe_row['minutes']} minutes

Ingredients:
{ingredient_text}

Steps:
{steps_text}
"""

        st.subheader("📝 Or Enter Your Own Recipe")

        recipe = st.text_area(
        "Recipe Input",
        value=dataset_recipe,
        height=300
        )

        st.subheader("🥗 Dietary Restrictions")

        diet = st.multiselect(
        "Select restrictions:",
        [
        "Vegan",
        "Vegetarian",
        "Gluten-Free",
        "Low-Carb",
        "High-Protein",
        "Diabetic",
        "Lactose-Free"
        ]
        )

        generate_btn = st.button("✨ Adapt Recipe")

    with col2:
        st.subheader("🤖 AI Generated Recipe")

    def generate_recipe(recipe, diet):

        prompt = f"""
You are an expert nutritionist and chef.

Input Recipe:
{recipe}

Dietary Restrictions:
{', '.join(diet)}

Provide:

1 Modified Recipe
2 Nutritional Information
3 Ingredient Substitutions with explanation
"""

        response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}]
        )

        return response.choices[0].message.content

    if generate_btn:

        if recipe:

            with st.spinner("AI is adapting your recipe... 🍳"):

                result = generate_recipe(recipe, diet)

            st.session_state["adapted_recipe"] = result
            st.session_state["original_recipe"] = recipe
            st.session_state["diet"] = diet

            with col2:

                st.markdown('<div class="box">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)

                st.download_button(
                "Download Adapted Recipe",
                result,
                file_name="adapted_recipe.txt"
                )

        else:
            st.warning("Please enter a recipe")

# -----------------------------
# NUTRITION TAB
# -----------------------------
elif menu == "Nutrition Insights":

    st.header("📊 Nutrition Insights")

    if "adapted_recipe" not in st.session_state:
        st.warning("Generate a recipe first")
    else:

        recipe_text = st.session_state["adapted_recipe"].lower()

        calories = 200
        protein = 10
        carbs = 20
        fat = 8

        if "tofu" in recipe_text:
            protein += 8
        if "olive oil" in recipe_text:
            fat += 10
        if "pasta" in recipe_text:
            carbs += 25
        if "rice" in recipe_text:
            carbs += 30

        data = {
        "Nutrient":["Calories","Protein","Carbs","Fat"],
        "Value":[calories,protein,carbs,fat]
        }

        df_nutrition = pd.DataFrame(data)

        st.table(df_nutrition)

# -----------------------------
# REPORT TAB
# -----------------------------
elif menu == "Report & Reviews":

    st.header("📑 Project Report")

    if "adapted_recipe" not in st.session_state:

        st.warning("Generate a recipe first")

    else:

        st.subheader("Original Recipe")
        st.write(st.session_state["original_recipe"])

        st.subheader("Adapted Recipe")
        st.write(st.session_state["adapted_recipe"])

        st.subheader("Dietary Restrictions Applied")
        st.write(", ".join(st.session_state["diet"]))

        st.subheader("Outcome")

        st.write("""
The AI system modified the recipe according to the selected dietary restrictions.
Ingredients were replaced with healthier or diet-compatible alternatives.
""")

        review_data = {
        "Original":["Chicken","Cream","Butter"],
        "Replacement":["Tofu","Coconut Milk","Olive Oil"],
        "Reason":[
        "Vegan protein source",
        "Dairy-free substitute",
        "Healthier fat option"
        ]
        }

        st.table(pd.DataFrame(review_data))

# -----------------------------
# VISUALIZATION TAB
# -----------------------------
elif menu == "Visualizations":

    st.header("📈 Nutrition Visualization")

    if "adapted_recipe" not in st.session_state:
        st.warning("Generate a recipe first")
    else:

        recipe_text = st.session_state["adapted_recipe"].lower()

        calories = 200
        protein = 10
        carbs = 20
        fat = 8

        if "tofu" in recipe_text:
            protein += 8
        if "olive oil" in recipe_text:
            fat += 10
        if "pasta" in recipe_text:
            carbs += 25
        if "rice" in recipe_text:
            carbs += 30

        nutrients = ["Calories","Protein","Carbs","Fat"]
        values = [calories,protein,carbs,fat]

        df_chart = pd.DataFrame({
        "Nutrient":nutrients,
        "Value":values
        })

        fig, ax = plt.subplots()
        ax.bar(df_chart["Nutrient"],df_chart["Value"])
        ax.set_title("Nutrition Breakdown")

        st.pyplot(fig)

        fig2 = px.pie(
        df_chart,
        values="Value",
        names="Nutrient",
        title="Nutrition Distribution"
        )

        st.plotly_chart(fig2)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("💡 Built with Streamlit + Groq (LLaMA)")