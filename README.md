# 📚 AI Offline Revision Assistant

An offline AI-powered study assistant that converts study PDFs into concise summaries, key revision points, and flashcards using locally running Large Language Models through Ollama.

## ✨ Features

- 📄 Upload study PDFs
- 📖 Generate concise study summaries
- 🎯 Extract important revision points
- 🧠 Generate exam-oriented flashcards
- 🤖 Support multiple local LLMs
- ⚡ Benchmark model inference performance
- 📊 Compare inference time, output speed, coverage, and relevance
- 🏆 Automatically recommend the better-performing model
- 🔒 No cloud AI API required
- 💾 Download generated revision material
- 📈 Display generation statistics
- ⏱️ Estimate processing time for uploaded documents

## 🤖 Supported Models

Currently benchmarked:

- `llama3.2:3b`
- `qwen2.5:3b`

The application uses Ollama to run the models locally.

## 🏗️ Project Architecture

```text
AI-offline revision-assistant/
│
├── app/
│   ├── app.py
│   ├── benchmark.py
│   ├── llm.py
│   ├── pdf_processor.py
│   ├── summarizer.py
│   ├── text_processor.py
│   │
│   └── tests/
│
├── evaluation/
│   ├── benchmark_report.py
│   ├── evaluation_dataset.py
│   ├── evaluator.py
│   ├── final_report.py
│   ├── relevance.py
│   └── run_evaluation.py
│
├── results/
│
├── data/
│
├── requirements.txt
├── .gitignore
└── README.md