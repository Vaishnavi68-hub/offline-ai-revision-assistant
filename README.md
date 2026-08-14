# 📚 AI Offline Revision Assistant

An AI-powered study assistant that transforms educational PDFs into **summaries, key points, and flashcards** using Large Language Models.

The project supports both **local AI inference using Ollama** and **cloud-based AI inference using Hugging Face**, making it flexible for both offline development and online deployment.

## 🚀 Live Demo

👉 **Hugging Face Space:**  
https://huggingface.co/spaces/vaishnavihuse134/offline-ai-revision-assistant-v2

---

## ✨ Features

- 📄 Upload study PDFs
- 🔍 Extract text from PDF documents
- 🧹 Clean and preprocess extracted text
- ✂️ Split large documents into manageable chunks
- 🤖 Generate AI-powered revision material
- 📝 Generate concise summaries
- 📌 Generate key points
- 🧠 Generate flashcards for revision
- 🖥️ Interactive Gradio web interface
- 🏠 Local AI inference using Ollama
- ☁️ Cloud AI inference using Hugging Face
- 🔄 Switch between local and cloud AI backends
- 🚀 Deployable on Hugging Face Spaces

---

## 🧠 AI Backends

The application supports two AI backends.

### 1. Local AI — Ollama

For local development, the application can use Ollama with:

**Model:** `qwen2.5:3b`

This allows the application to generate responses locally without sending prompts to a cloud API.

Set:

```bash
AI_BACKEND=local