#  Space-Weather-Intelligence-System (SSGI)

**Solar Storm & Geomagnetic Intelligence Platform** — An AI-powered space weather monitoring and briefing system.

Built for operational awareness, this system collects real-time solar data from NASA DONKI and NOAA, processes it intelligently, and delivers professional-grade space weather briefings powered by Retrieval-Augmented Generation (RAG) and Llama 3.

---

## ✨ Features

* 🌞 Real-time Solar Event Tracking (Solar Flares, CMEs, SEPs, Geomagnetic Storms)
* 🧠 Intelligent Retrieval with event-type detection and recency filtering
* 🎯 Cross-Encoder Reranking for high-quality contextual retrieval
* 🤖 Professional AI Briefings using structured Llama 3 prompts
* 💬 Interactive Chat Interface with chat history and persistence
* 📊 Live Sidebar Metrics (Sunspot Number, Solar Activity Indicators)
* 🔐 Secure Admin Portal with chat logging and management
* ⚙️ Modular Data Pipeline (Scrape → Clean → Chunk → Embed → Retrieve)

---

## 🛠️ Technology Stack

| Layer           | Technology                                |
| --------------- | ----------------------------------------- |
| Frontend        | Streamlit                                 |
| LLM Backend     | Ollama + Llama 3                          |
| Embeddings      | sentence-transformers (all-MiniLM-L6-v2)  |
| Reranker        | cross-encoder/ms-marco-MiniLM-L-6-v2      |
| Vector Database | FAISS                                     |
| Database        | SQLite                                    |
| Data Sources    | NASA DONKI API, NOAA SWPC                 |
| Orchestration   | Python Scripts (Cron Integration Planned) |

---

## 📁 Project Structure

```text
Astro-Knowledge-Assistant/

├── data/
│   ├── raw/
│   │   ├── NASA Archives
│   │   └── NOAA Raw Files
│   └── processed/
│       ├── Cleaned CSV Files
│       ├── documents.pkl
│       └── FAISS Index

├── docs/
│   ├── Architecture.md
│   └── progress.md

├── notebooks/

├── src/
│   ├── app.py
│   ├── ask_llama.py
│   ├── build_documents.py
│   ├── clean_master_dataset.py
│   ├── clean_nasa.py
│   ├── merge_datasets.py
│   ├── refine_forecast.py
│   ├── refine_noaa.py
│   ├── retriever.py
│   ├── solar_chunker.py
│   ├── update_master_live.py
│   ├── vector_store.py
│   └── web_scraper.py

├── launch.py
└── README.md
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Nardos-serkalem/Space-Weather-intelligence-System.git

cd Astro-Knowledge-Assistant-main
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Example requirements:

```txt
streamlit
pandas
faiss-cpu
sentence-transformers
transformers
torch
requests
python-dotenv
ollama
sqlite3
```

### 3. Install Ollama & Llama 3

Download Ollama:

https://ollama.com

Pull the Llama 3 model:

```bash
ollama pull llama3
```

---

## 🔑 Environment Setup

Create a `.env` file in the project root:

```env
NASA_API_KEY=your_nasa_api_key_here
```

---

## 🏗️ Build the Knowledge Base

### Step 1 — Fetch Latest Space Weather Data

```bash
python src/web_scraper.py
```

### Step 2 — Clean and Refine Datasets

```bash
python src/clean_nasa.py

python src/refine_noaa.py
```

### Step 3 — Generate Document Chunks

```bash
python src/build_documents.py
```

### Step 4 — Create the Vector Store

```bash
python src/vector_store.py
```

---

## ▶️ Run the Application

```bash
streamlit run src/app.py
```

---

## 🔐 Default Admin Credentials

```text
Username: ssgi_admin
Password: solar_2026
```

> Change the default credentials before deploying to production.

---

## 📊 Data Pipeline Workflow

```text
NASA DONKI API + NOAA SWPC
            │
            ▼
      Data Ingestion
            │
            ▼
      Data Cleaning
 (clean_nasa.py, refine_noaa.py)
            │
            ▼
     Solar Chunking
  (solar_chunker.py)
            │
            ▼
 Embedding & Indexing
 (FAISS + Sentence Transformers)
            │
            ▼
 Intelligent Retrieval
(Event Detection + Filtering)
            │
            ▼
 Cross-Encoder Reranking
            │
            ▼
 Grounded Llama 3 Generation
            │
            ▼
 Professional Space Weather Briefing
```

---

## 🎯 Use Cases

* Space Weather Monitoring Centers
* Solar Storm Intelligence & Forecasting
* GNSS and Satellite Operations Support
* Aviation and HF Communication Monitoring
* Research and Educational Applications
* Operational Space Situational Awareness

---

## 👨‍💻 Developed By

**Space Science and Geospatial Institute (SSGI)**

Machine Learning & Space Weather Intelligence Team

Addis Ababa, Ethiopia
