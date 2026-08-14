import os
import time

import streamlit as st
import ollama

from pdf_processor import (
    extract_text_from_pdf,
    clean_text
)

from text_processor import create_chunks

from summarizer import (
    summarize_chunk,
    create_final_summary,
    generate_key_points,
    generate_flashcards
)

from benchmark import (
    load_benchmark_results,
    calculate_model_averages,
    get_recommended_model
)

from cloud_llm import generate_cloud_response


# ==================================================
# CONFIGURATION
# ==================================================

CLOUD_MODEL = "meta-llama/Llama-3.2-3B-Instruct"

LOCAL_MODELS = [
    "llama3.2:3b",
    "qwen2.5:3b"
]


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Revision Assistant",
    page_icon="📚",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .feature-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        background-color: #fafafa;
        text-align: center;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">'
    '📚 AI Revision Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform your study PDFs into summaries, '
    'key points, and flashcards using local or '
    'cloud AI.'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("⚙️ Revision Settings")

    revision_mode = st.radio(
        "Choose revision mode:",
        [
            "Summary",
            "Key Points",
            "Flashcards"
        ]
    )

    st.divider()

    # ----------------------------------------------
    # AI MODE
    # ----------------------------------------------

    st.markdown("### 🤖 AI Mode")

    ai_mode = st.radio(
        "Choose where AI should run:",
        [
            "Local AI",
            "Cloud AI"
        ]
    )

    # ----------------------------------------------
    # LOCAL AI
    # ----------------------------------------------

    if ai_mode == "Local AI":

        st.markdown("### 💻 Local AI Model")

        model_name = st.selectbox(
            "Choose local AI model:",
            LOCAL_MODELS
        )

        st.info(
            f"Selected model: {model_name}\n\n"
            "Running locally through Ollama."
        )

        st.caption(
            "Your PDF content is processed locally."
        )

    # ----------------------------------------------
    # CLOUD AI
    # ----------------------------------------------

    else:

        model_name = CLOUD_MODEL

        st.markdown("### ☁️ Cloud AI Model")

        st.info(
            f"Selected model:\n"
            f"{CLOUD_MODEL}\n\n"
            "Running through Hugging Face Inference."
        )

        st.caption(
            "Cloud mode requires a valid HF_TOKEN "
            "environment variable."
        )

    # ----------------------------------------------
    # SYSTEM STATUS
    # ----------------------------------------------

    st.markdown("### 🟢 System Status")

    if ai_mode == "Local AI":

        try:

            available_models = ollama.list()

            model_names = [
                model["model"]
                for model in available_models["models"]
            ]

            model_available = (
                model_name in model_names
                or any(
                    name.startswith(model_name)
                    for name in model_names
                )
            )

            if model_available:

                st.success(
                    "Ollama: Connected"
                )

                st.success(
                    f"Model available: {model_name}"
                )

            else:

                st.warning(
                    "Ollama: Connected"
                )

                st.warning(
                    f"Model '{model_name}' "
                    "is not installed."
                )

                st.caption(
                    f"Run: ollama pull {model_name}"
                )

        except Exception:

            st.error(
                "Ollama: Not connected"
            )

            st.caption(
                "Start Ollama before generating "
                "local revision material."
            )

    else:

        hf_token = os.getenv("HF_TOKEN")

        if hf_token:

            st.success(
                "Hugging Face: Token detected"
            )

            st.success(
                "Cloud AI: Ready"
            )

        else:

            st.error(
                "Hugging Face: HF_TOKEN not found"
            )

            st.caption(
                "Set the HF_TOKEN environment "
                "variable before using Cloud AI."
            )

    # ----------------------------------------------
    # PRIVACY
    # ----------------------------------------------

    st.divider()

    st.markdown("### 🔒 Privacy")

    if ai_mode == "Local AI":

        st.success(
            "Local mode: your study material "
            "is processed on your computer. "
            "No cloud AI API is used."
        )

    else:

        st.warning(
            "Cloud mode: selected study content "
            "is sent to the configured cloud AI "
            "provider for generation."
        )

    # ----------------------------------------------
    # NEW DOCUMENT
    # ----------------------------------------------

    st.divider()

    if st.button(
        "🔄 New Document",
        use_container_width=True
    ):

        st.rerun()

    # ----------------------------------------------
    # BENCHMARK
    # ----------------------------------------------

    st.divider()

    with st.expander("📊 Model Benchmark"):

        benchmark_results = (
            load_benchmark_results()
        )

        if benchmark_results:

            averages = (
                calculate_model_averages(
                    benchmark_results
                )
            )

            recommended_model = (
                get_recommended_model(
                    averages
                )
            )

            if recommended_model:

                st.success(
                    f"🏆 Recommended model: "
                    f"{recommended_model}"
                )

            for model, metrics in averages.items():

                st.markdown(
                    f"**{model}**"
                )

                st.caption(
                    f"Inference: "
                    f"{metrics['inference_time']:.2f}s"
                )

                st.caption(
                    f"Output words: "
                    f"{metrics['output_words']:.2f}"
                )

                st.caption(
                    f"Speed: "
                    f"{metrics['speed']:.2f} words/s"
                )

                st.caption(
                    f"Coverage: "
                    f"{metrics['coverage']:.2f}%"
                )

                st.caption(
                    f"Relevance: "
                    f"{metrics['relevance']:.2f}%"
                )

                st.divider()

        else:

            st.info(
                "No benchmark results available."
            )


# ==================================================
# CLOUD PROMPT FUNCTIONS
# ==================================================

def cloud_summarize_chunk(text):
    """
    Summarize one document chunk using
    the configured cloud model.
    """

    prompt = f"""
You are an AI study assistant.

Summarize the following study material
for a student preparing for an exam.

Focus on:

- important concepts
- definitions
- key points
- formulas
- examples

Keep the explanation clear and concise.

Do not introduce information that is not
present in the study material.

Study material:

{text}
"""

    return generate_cloud_response(prompt)


def cloud_create_final_summary(chunk_summaries):
    """
    Create the final study summary using cloud AI.
    """

    combined_summaries = "\n\n".join(
        f"Section {i + 1}:\n{summary}"
        for i, summary in enumerate(
            chunk_summaries
        )
    )

    prompt = f"""
You are an AI revision assistant.

Create a comprehensive final study summary
from the section summaries below.

Requirements:

- Cover the most important concepts.
- Keep important definitions.
- Preserve important facts and relationships.
- Organize information using clear headings
  and bullet points.
- Remove unnecessary repetition.
- Do not introduce information that is not
  present in the provided summaries.
- Make the result useful for exam revision.

Section summaries:

{combined_summaries}
"""

    return generate_cloud_response(prompt)


def cloud_generate_key_points(chunk_summaries):
    """
    Generate important revision points using cloud AI.
    """

    combined_summaries = "\n\n".join(
        f"Section {i + 1}:\n{summary}"
        for i, summary in enumerate(
            chunk_summaries
        )
    )

    prompt = f"""
You are an AI revision assistant.

Extract the most important points from the
study material below.

Create concise exam-oriented revision notes.

Requirements:

- Focus on important concepts.
- Include important definitions.
- Include formulas or rules if present.
- Include important facts.
- Remove unnecessary explanations.
- Use bullet points.
- Do not add information that is not present
  in the material.

Study material:

{combined_summaries}
"""

    return generate_cloud_response(prompt)


def cloud_generate_flashcards(chunk_summaries):
    """
    Generate question-answer flashcards
    using cloud AI.
    """

    combined_summaries = "\n\n".join(
        f"Section {i + 1}:\n{summary}"
        for i, summary in enumerate(
            chunk_summaries
        )
    )

    prompt = f"""
You are an AI revision assistant.

Create useful study flashcards from the
material below.

Each flashcard must contain:

- Question
- Answer

Requirements:

- Focus on important concepts and definitions.
- Include important facts, formulas, rules,
  or relationships when present.
- Questions should test understanding
  and recall.
- Answers must be concise and accurate.
- Do not introduce information that is not
  present in the material.
- Create 10 to 15 flashcards if the material
  contains enough information.

Format the output exactly like this:

Q1: [question]
A1: [answer]

Q2: [question]
A2: [answer]

Study material:

{combined_summaries}
"""

    return generate_cloud_response(prompt)


# ==================================================
# UNIFIED AI GENERATION
# ==================================================

def generate_chunk_summary(text, ai_mode, model_name):
    """
    Route chunk summarization to Local or Cloud AI.
    """

    if ai_mode == "Local AI":

        return summarize_chunk(
            text,
            model_name
        )

    return cloud_summarize_chunk(text)


def generate_final_result(
    chunk_summaries,
    revision_mode,
    ai_mode,
    model_name
):
    """
    Route final generation to Local or Cloud AI.
    """

    if ai_mode == "Local AI":

        if revision_mode == "Summary":

            return create_final_summary(
                chunk_summaries,
                model_name
            )

        if revision_mode == "Key Points":

            return generate_key_points(
                chunk_summaries,
                model_name
            )

        return generate_flashcards(
            chunk_summaries,
            model_name
        )

    # ----------------------------------------------
    # CLOUD
    # ----------------------------------------------

    if revision_mode == "Summary":

        return cloud_create_final_summary(
            chunk_summaries
        )

    if revision_mode == "Key Points":

        return cloud_generate_key_points(
            chunk_summaries
        )

    return cloud_generate_flashcards(
        chunk_summaries
    )


# ==================================================
# FILE UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "📄 Upload your study PDF",
    type=["pdf"],
    help=(
        "Upload a text-based PDF containing "
        "your study material."
    )
)


# ==================================================
# LANDING PAGE
# ==================================================

if uploaded_file is None:

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
            <h3>📖 Smart Summary</h3>
            <p>
            Convert lengthy study material into
            concise revision notes.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">
            <h3>🎯 Key Points</h3>
            <p>
            Extract important concepts,
            definitions, and exam points.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">
            <h3>🧠 Flashcards</h3>
            <p>
            Generate question-answer cards
            for active recall.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# PDF PROCESSING
# ==================================================

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🚀 Generate Revision Material",
        type="primary",
        use_container_width=True
    ):

        # ------------------------------------------
        # VALIDATE AI CONFIGURATION
        # ------------------------------------------

        if ai_mode == "Local AI":

            try:

                available_models = ollama.list()

                model_names = [
                    model["model"]
                    for model in available_models["models"]
                ]

                model_available = (
                    model_name in model_names
                    or any(
                        name.startswith(model_name)
                        for name in model_names
                    )
                )

                if not model_available:

                    st.error(
                        f"Local model '{model_name}' "
                        "is not installed."
                    )

                    st.info(
                        f"Run:\n"
                        f"ollama pull {model_name}"
                    )

                    st.stop()

            except Exception as error:

                st.error(
                    "Ollama is not running."
                )

                st.info(
                    "Start Ollama and try again."
                )

                st.stop()

        else:

            if not os.getenv("HF_TOKEN"):

                st.error(
                    "HF_TOKEN environment variable "
                    "is not configured."
                )

                st.info(
                    "Set your Hugging Face token "
                    "as HF_TOKEN and restart "
                    "the terminal/application."
                )

                st.stop()

        # ------------------------------------------
        # SAVE PDF
        # ------------------------------------------

        os.makedirs(
            "data",
            exist_ok=True
        )

        temp_pdf_path = (
            "data/uploaded_notes.pdf"
        )

        with open(
            temp_pdf_path,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getvalue()
            )

        # ------------------------------------------
        # EXTRACT TEXT
        # ------------------------------------------

        with st.status(
            "📖 Reading PDF...",
            expanded=True
        ) as status:

            try:

                raw_text = extract_text_from_pdf(
                    temp_pdf_path
                )

                st.write(
                    f"Extracted "
                    f"{len(raw_text)} characters."
                )

                cleaned_text = clean_text(
                    raw_text
                )

                st.write(
                    f"Cleaned text: "
                    f"{len(cleaned_text)} characters."
                )

                if not cleaned_text.strip():

                    status.update(
                        label="❌ PDF processing failed",
                        state="error"
                    )

                    st.error(
                        "No readable text was found "
                        "in this PDF. Please upload a "
                        "text-based PDF."
                    )

                    st.stop()

                # ----------------------------------
                # CREATE CHUNKS
                # ----------------------------------

                st.write(
                    "Creating document chunks..."
                )

                chunks = create_chunks(
                    cleaned_text,
                    chunk_size=500,
                    overlap=50
                )

                if not chunks:

                    status.update(
                        label="❌ No chunks created",
                        state="error"
                    )

                    st.error(
                        "The document could not be "
                        "divided into text chunks."
                    )

                    st.stop()

                st.write(
                    f"Created {len(chunks)} "
                    "text chunks."
                )

                # ----------------------------------
                # PROCESSING TIME ESTIMATE
                # ----------------------------------

                if ai_mode == "Local AI":

                    estimated_seconds = (
                        len(chunks) * 8
                    )

                else:

                    estimated_seconds = (
                        len(chunks) * 4
                    )

                estimated_minutes = (
                    estimated_seconds / 60
                )

                if estimated_minutes < 1:

                    st.info(
                        f"⏱️ Estimated AI processing "
                        f"time: "
                        f"{estimated_seconds:.0f} seconds"
                    )

                else:

                    st.info(
                        f"⏱️ Estimated AI processing "
                        f"time: approximately "
                        f"{estimated_minutes:.1f} minutes"
                    )

                status.update(
                    label="✅ PDF processed successfully",
                    state="complete"
                )

            except Exception as error:

                status.update(
                    label="❌ PDF processing failed",
                    state="error"
                )

                st.error(
                    f"Unable to process PDF: {error}"
                )

                st.stop()

        # ------------------------------------------
        # DOCUMENT INFORMATION
        # ------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Characters",
                len(cleaned_text)
            )

        with col2:

            st.metric(
                "Chunks",
                len(chunks)
            )

        with col3:

            st.metric(
                "AI Model",
                model_name
            )

        st.markdown("---")

        # ------------------------------------------
        # AI PROCESSING
        # ------------------------------------------

        if ai_mode == "Local AI":

            st.subheader(
                "🤖 Processing with Local AI"
            )

        else:

            st.subheader(
                "☁️ Processing with Cloud AI"
            )

        chunk_summaries = []

        progress = st.progress(
            0,
            text="Starting AI processing..."
        )

        generation_start = time.time()

        try:

            for i, chunk in enumerate(chunks):

                progress.progress(
                    (i + 1) / len(chunks),
                    text=(
                        f"Processing section "
                        f"{i + 1} of {len(chunks)}..."
                    )
                )

                summary = generate_chunk_summary(
                    chunk,
                    ai_mode,
                    model_name
                )

                chunk_summaries.append(
                    summary
                )

        except RuntimeError as error:

            progress.empty()

            st.error(
                f"❌ {error}"
            )

            if ai_mode == "Local AI":

                st.info(
                    "Make sure Ollama is running "
                    f"and that '{model_name}' "
                    "is installed."
                )

            else:

                st.info(
                    "Check your HF_TOKEN and "
                    "Hugging Face cloud inference "
                    "configuration."
                )

            st.stop()

        except Exception as error:

            progress.empty()

            st.error(
                f"❌ AI generation failed: {error}"
            )

            st.stop()

        progress.empty()

        # ------------------------------------------
        # GENERATE FINAL RESULT
        # ------------------------------------------

        try:

            if revision_mode == "Summary":

                with st.spinner(
                    "Creating final study summary..."
                ):

                    result = generate_final_result(
                        chunk_summaries,
                        revision_mode,
                        ai_mode,
                        model_name
                    )

            elif revision_mode == "Key Points":

                with st.spinner(
                    "Extracting key revision points..."
                ):

                    result = generate_final_result(
                        chunk_summaries,
                        revision_mode,
                        ai_mode,
                        model_name
                    )

            else:

                with st.spinner(
                    "Creating flashcards..."
                ):

                    result = generate_final_result(
                        chunk_summaries,
                        revision_mode,
                        ai_mode,
                        model_name
                    )

        except RuntimeError as error:

            st.error(
                f"❌ {error}"
            )

            st.stop()

        except Exception as error:

            st.error(
                f"❌ Final generation failed: {error}"
            )

            st.stop()

        generation_time = (
            time.time() - generation_start
        )

        # ------------------------------------------
        # GENERATION METRICS
        # ------------------------------------------

        output_words = len(
            result.split()
        )

        if generation_time > 0:

            output_speed = (
                output_words /
                generation_time
            )

        else:

            output_speed = 0

        st.markdown("---")

        st.subheader(
            "📊 Generation Metrics"
        )

        metric1, metric2, metric3, metric4 = (
            st.columns(4)
        )

        with metric1:

            st.metric(
                "Generation Time",
                f"{generation_time:.2f} s"
            )

        with metric2:

            st.metric(
                "Output Words",
                output_words
            )

        with metric3:

            st.metric(
                "Output Speed",
                f"{output_speed:.2f} words/s"
            )

        with metric4:

            st.metric(
                "Chunks",
                len(chunks)
            )

        # ------------------------------------------
        # DISPLAY RESULT
        # ------------------------------------------

        st.markdown("---")

        if revision_mode == "Summary":

            st.success(
                f"Study summary generated "
                f"using {ai_mode}!"
            )

            st.markdown(
                "## 📖 Study Summary"
            )

            st.markdown(result)

            st.download_button(
                label="⬇️ Download Summary",
                data=result,
                file_name="study_summary.txt",
                mime="text/plain"
            )

        elif revision_mode == "Key Points":

            st.success(
                f"Key points generated "
                f"using {ai_mode}!"
            )

            st.markdown(
                "## 🎯 Key Revision Points"
            )

            st.markdown(result)

            st.download_button(
                label="⬇️ Download Key Points",
                data=result,
                file_name="key_points.txt",
                mime="text/plain"
            )

        else:

            st.success(
                f"Flashcards generated "
                f"using {ai_mode}!"
            )

            st.markdown(
                "## 🧠 Flashcards"
            )

            st.markdown(result)

            st.download_button(
                label="⬇️ Download Flashcards",
                data=result,
                file_name="flashcards.txt",
                mime="text/plain"
            )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "🔒 AI Revision Assistant • "
    "Local Ollama + Hugging Face Cloud AI"
)