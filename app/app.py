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


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Offline Revision Assistant",
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
    '📚 AI Offline Revision Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform your study PDFs into summaries, '
    'key points, and flashcards using a '
    'locally running AI model.'
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
    # AI MODEL
    # ----------------------------------------------

    st.markdown("### 🤖 AI Model")

    model_name = st.selectbox(
        "Choose local AI model:",
        [
            "llama3.2:3b",
            "qwen2.5:3b"
        ]
    )

    st.info(
        f"Selected model: {model_name}\n\n"
        "Running locally through Ollama."
    )

    # ----------------------------------------------
    # SYSTEM STATUS
    # ----------------------------------------------

    st.markdown("### 🟢 System Status")

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

            st.success("Ollama: Connected")

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
            "revision material."
        )

    # ----------------------------------------------
    # PRIVACY
    # ----------------------------------------------

    st.divider()

    st.markdown("### 🔒 Privacy")

    st.success(
        "Your study material stays on your "
        "computer. No cloud AI API is required."
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

            # --------------------------------------
            # MODEL RECOMMENDATION
            # --------------------------------------

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

            # --------------------------------------
            # MODEL METRICS
            # --------------------------------------

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
                    chunk_size=100,
                    overlap=20
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
        # LOCAL AI PROCESSING
        # ------------------------------------------

        st.subheader(
            "🤖 Processing with Local AI"
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

                summary = summarize_chunk(
                    chunk,
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

            st.info(
                "Make sure Ollama is running and "
                f"that '{model_name}' is installed."
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

                    result = create_final_summary(
                        chunk_summaries,
                        model_name
                    )

            elif revision_mode == "Key Points":

                with st.spinner(
                    "Extracting key revision points..."
                ):

                    result = generate_key_points(
                        chunk_summaries,
                        model_name
                    )

            else:

                with st.spinner(
                    "Creating flashcards..."
                ):

                    result = generate_flashcards(
                        chunk_summaries,
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
                "Study summary generated!"
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
                "Key points generated!"
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
                "Flashcards generated!"
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
    "🔒 Offline AI • Ollama • Local LLMs • "
    "Your study material remains local"
)