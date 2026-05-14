import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.set_page_config(page_title="Review Analyzer", layout="centered")

st.title("Product Review Analyzer")

product_name = st.text_input("Product name or URL")

review_text = st.text_area(
    "Paste product reviews here",
    height=280,
    placeholder="Paste at least 15-20 reviews..."
)

def analyze_reviews(product, reviews):
    prompt = f"""
Analyze these product reviews and give useful insights.

Product:
{product}

Reviews:
{reviews}

Please provide:
- Common complaints
- Positive points
- Overall sentiment
- Short ad copy
- 3 marketing hooks
- Image generation prompt
- Video ad prompt
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=1000
    )

    return response.choices[0].message.content


if st.button("Analyze"):
    if product_name.strip() == "":
        st.warning("Please enter a product name or URL.")
    elif review_text.strip() == "":
        st.warning("Please paste some reviews first.")
    else:
        with st.spinner("Analyzing reviews..."):
            result = analyze_reviews(product_name, review_text)

        st.subheader("Result")
        st.write(result)