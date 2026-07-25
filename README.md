# Review Extraction Pipeline

An end-to-end pipeline that extracts structured insights—key themes, sentiment, pros, cons, and reviewer details—from raw product reviews using **LangChain**, **Groq (Llama 3.1)**, **FastAPI**, and **MongoDB Atlas**, with a **Streamlit** dashboard interface.
<img width="1470" height="836" alt="image" src="https://github.com/user-attachments/assets/484c8e71-ba41-483e-9b2c-cb868cbc65fc" />
<img width="1468" height="833" alt="image" src="https://github.com/user-attachments/assets/3a1d3605-0bd6-4a30-b7eb-1c7af982a599" />

---

## Features

- **Structured LLM Extraction**: Converts unstructured review text into structured JSON models via Pydantic & Groq.
- **Sentiment & Theme Tagging**: Classifies reviews (`pos`, `neg`, `neutral`) and extracts key topics.
- **MongoDB Persistence**: Stores extracted review insights with fallback handling.
- **REST API**: FastAPI endpoints for real-time analysis and fetching historical reviews.
- **Minimal Dashboard**: Streamlit web interface with search, metrics, and filtering.

---

## Tech Stack

- **LLM Engine**: LangChain (`langchain-groq`), Llama 3.1 8B Instant
- **Backend API**: FastAPI, Uvicorn
- **Frontend UI**: Streamlit
- **Database**: MongoDB Atlas (`pymongo`)
- **Validation**: Pydantic v2

---

## Project Structure

```
.
├── app.py           # Streamlit dashboard interface
├── main.py          # FastAPI backend server
├── extractor.py     # Core LLM extraction & MongoDB logic
├── requirements.txt # Python dependencies
└── .env             # Environment configuration
```

---

## Setup & Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/rahulchaudhh/Review-Extraction-Pipeline.git
cd Review-Extraction-Pipeline
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
MONGO_URI=your_mongodb_atlas_uri
API_URL=http://127.0.0.1:8000
```

### 3. Run Application

**Start Backend API (FastAPI):**
```bash
uvicorn main:app --reload
```
*API running at `http://127.0.0.1:8000` (Interactive docs at `http://127.0.0.1:8000/docs`)*

**Start Frontend UI (Streamlit):**
```bash
streamlit run app.py
```
*Dashboard running at `http://localhost:8501`*

---

## API Endpoints

- `POST /analyze` - Analyze raw review text and return/store structured data.
- `GET /reviews` - Fetch stored reviews from MongoDB.

---

## License

MIT
