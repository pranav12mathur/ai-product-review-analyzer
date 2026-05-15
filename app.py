import os
import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
st.set_page_config(page_title="AI Product Review Analyzer", layout="centered")
st.title("AI Product Review Analyzer")
product_name = st.text_input("Enter product name")
def scrape_reviews(product, limit=20):
    reviews = []
    headers = {
        "User-Agent": "product-review-analyzer/1.0"
    }
    search_url = "https://www.reddit.com/search.json"
    params = {
        "q": f"{product} review",
        "limit": 8,
        "sort": "relevance",
        "raw_json": 1
    }
    try:
        search_response = requests.get(
            search_url,
            headers=headers,
            params=params,
            timeout=15
        )
        if search_response.status_code != 200:
            return []
        search_data = search_response.json()
        posts = search_data.get("data", {}).get("children", [])
        for post in posts:
            post_data = post.get("data", {})
            permalink = post_data.get("permalink")
            title = post_data.get("title", "")
            selftext = post_data.get("selftext", "")
            if title and len(title) > 30:
                reviews.append(title)
            if selftext and len(selftext) > 50:
                reviews.append(selftext)
            if permalink:
                comments_url = "https://www.reddit.com" + permalink + ".json"
                comments_response = requests.get(
                    comments_url,
                    headers=headers,
                    params={"raw_json": 1},
                    timeout=15
                )
                if comments_response.status_code == 200:
                    comments_data = comments_response.json()
                    if len(comments_data) > 1:
                        comments = comments_data[1].get("data", {}).get("children", [])
                        for comment in comments:
                            comment_data = comment.get("data", {})
                            body = comment_data.get("body", "")
                            if body and len(body) > 40:
                                if body not in reviews:
                                    reviews.append(body)
                            if len(reviews) >= limit:
                                break
            if len(reviews) >= limit:
                break
    except Exception:
        return []
    return reviews[:limit]
def analyze_reviews(product, reviews):
    prompt = f"""
You are analyzing customer reviews for a product.
Product:
{product}
Reviews:
{reviews}
Generate the output in this format:
1. Common complaints
2. Positive highlights
3. Overall sentiment summary
4. Short ad copy
5. 3 marketing hooks
6. One AI image generation prompt
7. One AI video ad prompt
Keep the answer simple and practical.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=1200
    )
    return response.choices[0].message.content
if "review_text" not in st.session_state:
    st.session_state.review_text = ""
col1, col2 = st.columns(2)
with col1:
    if st.button("Scrape Reviews"):
        if product_name.strip() == "":
            st.warning("Please enter a product name first.")
        else:
            with st.spinner("Scraping reviews..."):
                scraped_reviews = scrape_reviews(product_name)
            if len(scraped_reviews) == 0:
                st.error("No reviews found. Try another popular product name.")
            else:
                st.session_state.review_text = "\n\n".join(scraped_reviews)
                st.success(f"Scraped {len(scraped_reviews)} reviews/comments.")
with col2:
    if st.button("Clear Reviews"):
        st.session_state.review_text = ""
review_text = st.text_area(
    "Reviews / Comments",
    value=st.session_state.review_text,
    height=300,
    placeholder="Scraped reviews will appear here. You can also paste reviews manually."
)
st.session_state.review_text = review_text
if st.button("Analyze Reviews"):
    if product_name.strip() == "":
        st.warning("Please enter a product name.")
    elif review_text.strip() == "":
        st.warning("Please scrape or paste reviews first.")
    else:
        with st.spinner("Analyzing reviews..."):
            result = analyze_reviews(product_name, review_text)
        st.subheader("AI Analysis Result")
        st.write(result)