# 📚 AI Offline Revision Assistant

An offline AI-powered study assistant that converts study PDFs into:

- 📖 Study summaries
- 🎯 Key revision points
- 🧠 Flashcards

The application uses local Large Language Models through Ollama, so study material does not need to be sent to a cloud AI API.

## ✨ Features

- Upload study PDFs
- Extract and clean PDF text
- Split documents into chunks
- Generate AI summaries
- Generate exam-oriented key points
- Generate flashcards
- Choose between local AI models
- View generation metrics
- Download generated revision material
- Reset and process a new document
- Fully local AI inference

## 🤖 Supported Models

Currently tested:

- `llama3.2:3b`
- `qwen2.5:3b`

The models run locally using Ollama.

## 🛠️ Tech Stack

- Python
- Streamlit
- Ollama
- Llama 3.2 3B
- Qwen 2.5 3B
- PyMuPDF
- Pandas
- Git / GitHub

## 📂 Project Structure

```text
AI-offline-revision-assistant/
│
├── app/
│   ├── app.py
│   ├── llm.py
│   ├── pdf_processor.py
│   ├── text_processor.py
│   └── summarizer.py
│
├── evaluation/
│   ├── evaluation_dataset.py
│   ├── evaluator.py
│   ├── final_report.py
│   └── run_evaluation.py
│
├── data/
├── results/
├── requirements.txt
├── .gitignore
└── README.md