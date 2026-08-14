import gradio as gr
import tempfile

from app.pdf_processor import extract_text_from_pdf, clean_text
from app.text_processor import create_chunks
from app.summarizer import (
    summarize_chunk,
    create_final_summary,
    generate_key_points,
    generate_flashcards
)


def process_pdf(pdf_file, revision_mode):

    if pdf_file is None:
        return "Please upload a PDF first."

    try:
        with open(pdf_file, "rb") as source:
            pdf_bytes = source.read()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(pdf_bytes)
            temp_pdf_path = temp_file.name

        raw_text = extract_text_from_pdf(temp_pdf_path)
        cleaned_text = clean_text(raw_text)

        if not cleaned_text.strip():
            return "❌ No readable text was found in the PDF."

        chunks = create_chunks(
            cleaned_text,
            chunk_size=500,
            overlap=50
        )

        if not chunks:
            return "❌ No text chunks were created."

        chunk_summaries = []

        for chunk in chunks:
            summary = summarize_chunk(chunk)
            chunk_summaries.append(summary)

        if revision_mode == "Summary":
            result = create_final_summary(chunk_summaries)

        elif revision_mode == "Key Points":
            result = generate_key_points(chunk_summaries)

        else:
            result = generate_flashcards(chunk_summaries)

        return result

    except Exception as error:
        return f"❌ Error: {error}"


with gr.Blocks(
    title="AI Offline Revision Assistant"
) as demo:

    gr.Markdown(
        """
        # 📚 AI Offline Revision Assistant

        Transform your study PDFs into
        **summaries, key points, and flashcards**
        using AI.
        """
    )

    with gr.Row():

        pdf_file = gr.File(
            label="📄 Upload Study PDF",
            file_types=[".pdf"],
            type="filepath"
        )

        revision_mode = gr.Radio(
            choices=[
                "Summary",
                "Key Points",
                "Flashcards"
            ],
            value="Summary",
            label="🎯 Revision Mode"
        )

    generate_button = gr.Button(
        "🚀 Generate Revision Material",
        variant="primary"
    )

    result = gr.Markdown()

    generate_button.click(
        fn=process_pdf,
        inputs=[pdf_file, revision_mode],
        outputs=result
    )


if __name__ == "__main__":
    demo.launch()
