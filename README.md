# RAG Medical QA Project 🏥

A **Retrieval-Augmented Generation (RAG)** system for medical document question-answering using Google's Gemini API, LangChain, and FAISS vector store.

## 📋 Project Structure

```
rag-project/
├── data/                        # Put your ZIP's extracted PDFs here (do NOT commit large files)
│   ├── doc1.pdf
│   ├── doc2.pdf
│   └── ...
├── src/
│   ├── ingest.py               # Parse PDFs, chunk text, create embeddings, persist vectorstore
│   ├── vectorstore/            # Directory where vectorstore files are saved (FAISS index + metadata)
│   ├── retriever.py            # Retrieval + answer generation helper functions
│   ├── utils.py                # Helper utilities (PDF parsing, chunking)
│   └── api/
│       ├── main.py             # FastAPI app implementing the evaluator API
│       └── requirements.txt    # Runtime requirements (app-local)
├── tests/
│   └── test_query.sh           # Example curl test script
├── .env.sample                 # Sample environment variables (copy to .env)
├── .gitignore                  # Git ignore configuration
├── Dockerfile                  # Containerize the app for deployment
├── docker-compose.yml          # Optional Docker Compose for local dev
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google API Key (for Gemini and embeddings)
- PDF documents for ingestion

### 1. Clone and Setup

```bash
cd rag-project

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy sample env file
cp .env.sample .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Add Your Documents

Place your PDF files in the `data/` directory:

```bash
# Example:
cp /path/to/your/medical_docs/*.pdf data/
```

### 4. Ingest Documents

Run the ingestion script to process PDFs and create the vector store:

```bash
python src/ingest.py
```

This will:
- Load all PDFs from `data/`
- Split documents into chunks
- Generate embeddings using sentence-transformers
- Create and save a FAISS index in `data/faiss_index/`

### 5. Run the API

Start the FastAPI server:

```bash
python src/api/main.py
```

The API will be available at `http://localhost:8000`

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 6. Test the API

Use the provided test script:

```bash
chmod +x tests/test_query.sh
./tests/test_query.sh
```

Or test manually with curl:

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the symptoms of diabetes?", "top_k": 5}'
```

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build the image
docker build -t rag-medical-qa .

# Run the container
docker run -p 8000:8000 --env-file .env rag-medical-qa
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📚 API Endpoints

### `GET /`
Root endpoint - Returns API information

### `GET /health`
Health check endpoint

### `POST /query`
Query the RAG system

**Request Body:**
```json
{
  "query": "What are the common treatments for hypertension?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Based on the documents...",
  "contexts": [
    "Context chunk 1...",
    "Context chunk 2...",
    "..."
  ]
}
```

## 🔧 Configuration

Key environment variables in `.env`:

- `GOOGLE_API_KEY`: Your Google API key (required)
- `VECTORSTORE_PATH`: Path to FAISS index (default: `./src/vectorstore/faiss_index`)
- `EMBEDDING_MODEL`: Google embedding model (default: `models/embedding-001`)
- `LLM_MODEL`: Gemini model for generation (default: `gemini-1.5-flash`)
- `PORT`: API server port (default: `8000`)

## 📝 Development

### Project Components

1. **ingest.py**: Document ingestion pipeline
   - Loads PDFs using PyPDFLoader
   - Splits text into chunks
   - Generates embeddings with sentence-transformers
   - Builds FAISS index

2. **retriever.py**: RAG retrieval and generation
   - Loads FAISS vectorstore
   - Performs similarity search
   - Generates answers using Gemini

3. **utils.py**: Helper functions
   - PDF loading utilities
   - Text chunking functions

4. **api/main.py**: FastAPI application
   - REST API endpoints
   - Request/response models
   - Error handling

### Running Tests

```bash
# Make test script executable
chmod +x tests/test_query.sh

# Run tests
./tests/test_query.sh
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/
```

## 🛠️ Troubleshooting

### Issue: "No documents found in vectorstore"
**Solution**: Run `python src/ingest.py` to create the vector index first.

### Issue: "Could not load vectorstore"
**Solution**: Ensure the `VECTORSTORE_PATH` in `.env` matches where you ran ingestion.

### Issue: API key errors
**Solution**: Verify your `GOOGLE_API_KEY` is set correctly in `.env`

### Issue: CUDA/GPU errors
**Solution**: The ingestion script auto-detects available devices (CUDA/MPS/CPU). For CPU-only, it will work but be slower.

## 📄 License

This project is for educational and hackathon purposes.

## 🤝 Contributing

Feel free to open issues or submit pull requests for improvements!

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API](https://ai.google.dev/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Built with ❤️ for Hack a Cure**
# vithackathon
