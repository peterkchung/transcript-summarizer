import streamlit as st
import requests

st.title('PDF Summarizer')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with st.spinner('Uploading and Summarizing...'):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://127.0.0.1:8000/upload/", files=files)
        data = response.json()

    st.write('## Summary:')
    st.write(data["summary"])