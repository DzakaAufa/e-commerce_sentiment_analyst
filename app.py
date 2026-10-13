import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import re

# 1. Konfigurasi Halaman UI
st.set_page_config(page_title="Sentiment Analysis App", layout="centered")
st.title("📊 Text Sentiment Analyst")
st.write("Input text or review in field below to detect the sentiment.")

# 2. Load Model dengan Cache
@st.cache_resource
def load_sentiment_model():
    model_path = "dzakaaufa/e_commerce-sentiment-analysis" 

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return tokenizer, model

tokenizer, model = load_sentiment_model()

# 3. Fungsi Preprocessing
def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s\s+", " ", text)
    return text.strip().lower()

# 4. Form Input User
user_input = st.text_area("Input text:", placeholder="Example: The product is safe and the delivery is on-time!")

# 5. Eksekusi Prediksi
if st.button("Analyst text", type="primary"):
    if user_input.strip() != "":
        # Preprocessing & Tokenisasi
        cleaned = clean_text(user_input)
        inputs = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True, max_length=128)
        
        # Inference
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            prediction = torch.argmax(probs, dim=1).item()
        
        # Pemetaan Label (Sesuaikan dengan dataset Anda)
        label_map = {0: "Negative 😡", 1: "Neutral 😐", 2: "Positive 😊"}
        result_label = label_map.get(prediction, "Tidak Diketahui")
        
        # Tampilkan Hasil di UI
        st.subheader("Prediction Result:")
        st.success(f"Sentiment: **{result_label}**")
        st.write(f"Text after cleaned: {cleaned}")

    else:
        st.warning("Please input the text first!")