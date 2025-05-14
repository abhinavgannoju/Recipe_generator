import streamlit as st
import requests

# ---------- CONFIGURATION ----------
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"  # Example model from Groq

# ---------- FUNCTION TO USE GROQ API (LLaMA 3) ----------
def generate_recipes_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional chef. Provide exactly three different Indian recipes with detailed ingredients and instructions with proper timings and mention number of servings, ensuring variety in ingredients and cooking styles, without any starting or ending texts,end every recipe with ||."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 2000
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        recipe_text = response.json()['choices'][0]['message']['content']
        
        # Split recipes assuming they are separated by double newlines or some clear marker
        recipes = recipe_text.split("||")  # Adjust splitting logic if needed
        return recipes[:3]  # Ensure only 3 recipes are returned
    else:
        return [f"Error from Groq: {response.status_code} - {response.text}"]

# ---------- STREAMLIT APP ----------
def main():
    st.set_page_config(page_title="AI Recipe Generator", page_icon="🍽️", layout="centered")
    st.title("🍽️ AI Recipe Generator ")

    # User input
    recipe_name = st.text_input("Enter your recipe name:")
    if recipe_name:
        user_prompt = f"Give me three distinct Indian recipe names for {recipe_name} with detailed ingredients and instructions with proper timings and number of servings, without any starting or ending texts,end every recipe with ||."
    else:
        user_prompt = ""

    if st.button("Generate Recipes"):
        if not recipe_name.strip():
            st.warning("Please enter a recipe name!")
            return

        with st.spinner("Generating recipes..."):
            groq_recipes = generate_recipes_groq(user_prompt)

        if len(groq_recipes) < 3:
            st.error("Could not generate three recipes. Please try again!")
            return
        col1, space1, col2, space2, col3 = st.columns([3, 6 , 3, 6, 3])  
        # Display recipes side by side
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🍛 Recipe 1")
            st.write(groq_recipes[0])

        with col2:
            st.subheader("🍲 Recipe 2")
            st.write(groq_recipes[1])

        with col3:
            st.subheader("🥘 Recipe 3")
            st.write(groq_recipes[2])

# ---------- MAIN ----------
if __name__ == "__main__":
    main()
