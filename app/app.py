import streamlit as st

from pdf_processor import extract_text_from_pdf


st.set_page_config(
    page_title="Offline AI Revision Assistant",
    page_icon="📚"
)

st.title("📚 Offline AI Revision Assistant")

st.write(
    "Upload your study notes in PDF format."
)

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("PDF uploaded successfully!")

    with open("temp.pdf", "wb") as file:
        file.write(uploaded_file.getbuffer())

    text = extract_text_from_pdf("temp.pdf")

    st.subheader("Extracted Text")

    st.text_area(
        "PDF Content",
        text,
        height=400
    )