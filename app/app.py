import streamlit as st

from pdf_processor import extract_text_from_pdf, clean_text
from text_processor import create_chunks
from summarizer import (
    summarize_chunk,
    create_final_summary,
    generate_key_points,
    generate_flashcards
)


st.set_page_config(
    page_title="AI Offline Revision Assistant",
    page_icon="📚",
    layout="wide"
)


st.title("📚 AI Offline Revision Assistant")

st.write(
    "Upload your study PDF and generate revision material "
    "using a local AI model."
)


uploaded_file = st.file_uploader(
    "Upload your study PDF",
    type=["pdf"]
)


revision_mode = st.radio(
    "Choose revision mode:",
    [
        "Summary",
        "Key Points",
        "Flashcards"
    ],
    horizontal=True
)


if uploaded_file is not None:

    st.success("PDF uploaded successfully.")

    if st.button("Generate"):

        with st.spinner("Reading PDF..."):

            pdf_bytes = uploaded_file.getvalue()

            temp_pdf_path = "data/uploaded_notes.pdf"

            with open(temp_pdf_path, "wb") as file:
                file.write(pdf_bytes)

            raw_text = extract_text_from_pdf(temp_pdf_path)

            cleaned_text = clean_text(raw_text)

        if not cleaned_text.strip():

            st.error(
                "No readable text was found in this PDF. "
                "Please upload a text-based PDF."
            )

        else:

            with st.spinner("Creating document chunks..."):

                chunks = create_chunks(
                    cleaned_text,
                    chunk_size=100,
                    overlap=20
                )

            st.info(f"Created {len(chunks)} text chunks.")

            chunk_summaries = []

            progress = st.progress(0)

            for i, chunk in enumerate(chunks):

                with st.spinner(
                    f"Processing section {i + 1} of {len(chunks)}..."
                ):

                    summary = summarize_chunk(chunk)

                    chunk_summaries.append(summary)

                progress.progress((i + 1) / len(chunks))

            if revision_mode == "Summary":

                with st.spinner("Creating final study summary..."):

                    result = create_final_summary(
                        chunk_summaries
                    )

                st.success("Summary generated!")

                st.markdown("## 📖 Study Summary")

                st.markdown(result)

            elif revision_mode == "Key Points":

                with st.spinner("Extracting key revision points..."):

                    result = generate_key_points(
                        chunk_summaries
                    )

                st.success("Key points generated!")

                st.markdown("## 🎯 Key Revision Points")

                st.markdown(result)

            elif revision_mode == "Flashcards":

                with st.spinner("Creating flashcards..."):

                    result = generate_flashcards(
                        chunk_summaries
                    )

                st.success("Flashcards generated!")

                st.markdown("## 🧠 Flashcards")

                st.markdown(result)