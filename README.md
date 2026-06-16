# Space-Weather-intelligence-System (SSGI)
Solar Storm & Geomagnetic Intelligence Platform — An AI-powered space weather monitoring and briefing system.

Built for operational awareness, this system collects real-time solar data from NASA DONKI and NOAA, processes it intelligently, and delivers professional-grade space weather briefings powered by Retrieval-Augmented Generation (RAG) and Llama 3.

✨ Features
Real-time Solar Event Tracking (Flares, CMEs, SEPs, Geomagnetic Storms)
Intelligent Retrieval with event-type detection and recency filtering
Cross-Encoder Reranking for high-quality context
Professional AI Briefings using structured Llama 3 prompts
Interactive Chat Interface with history and persistence
Live Sidebar Metrics (Sunspot Number, etc.)
Secure Admin Portal with chat logging
Modular Data Pipeline (scrape → clean → chunk → embed)
🛠️ Tech Stack
Layer	Technology
Frontend	Streamlit
Backend LLM	Ollama + Llama 3
Embeddings	sentence-transformers (all-MiniLM-L6-v2)
Reranker	cross-encoder/ms-marco-MiniLM-L-6-v2
Vector Database	FAISS
Database	SQLite
Data Sources	NASA DONKI API, NOAA SWPC
Orchestration	Python scripts + cron (planned)
📁 Project Structure
astro-knowledge-assistant/
├── data/
│   ├── raw/                    # NASA archives, NOAA raw files
│   └── processed/              # Cleaned CSVs, documents.pkl, FAISS index
├── src/                        # (optional) future source organization
├── attachments/                # Core scripts (for reference)
│   ├── web_scraper.py
│   ├── clean_nasa.py
│   ├── refine_noaa.py
│   ├── solar_chunker.py
│   ├── build_documents.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── app.py
└── README.md
🚀 Installation & Setup
1. Clone the Repository
git clone git@github.com:benayascode/Astro-Knowledge-Assistant.git
cd astro-knowledge-assistant
2. Install Dependencies
pip install -r requirements.txt
(Create a requirements.txt with the following if you haven't already:)

streamlit
pandas
faiss-cpu
sentence-transformers
cross-encoder
ollama
requests
python-dotenv
sqlite3
3. Install Ollama + Llama 3
# Download Ollama from https://ollama.com
ollama pull llama3
4. Environment Setup
Create a .env file in the root:

NASA_API_KEY=your_nasa_api_key_here
5. Build the Knowledge Base
Run the full pipeline:

# 1. Fetch latest data
python src/web_scraper.py

# 2. Clean datasets
python src/clean_nasa.py
python src/refine_noaa.py

# 3. Build document chunks
python src/build_documents.py

# 4. Create vector store
python src/vector_store.py
6. Run the Application
streamlit run src/app.py
Default credentials:

Username: ssgi_admin
Password: solar_2026
📊 Data Pipeline Workflow
Ingestion → NASA DONKI API + NOAA text files
Cleaning → clean_nasa.py, refine_noaa.py
Chunking → Domain-specific solar_chunker.py
Embedding & Indexing → FAISS + Sentence Transformers
Retrieval → Smart filtering + Cross-Encoder reranking
Generation → Grounded Llama 3 briefing
