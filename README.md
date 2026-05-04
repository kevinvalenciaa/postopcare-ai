# PostOpCare AI

> Evidence-based, patient-friendly post-operative recovery handouts, generated in seconds and grounded in real medical literature.

PostOpCare AI helps clinicians produce trustworthy after-surgery instructions for their patients. A clinician picks a procedure, the system retrieves relevant evidence from PubMed and clinical guidelines, and a large language model writes a six-section recovery guide at a 6th to 8th grade reading level. Every claim is backed by an inline citation, and every handout gets a shareable public link plus a printable QR code that the front desk can hand to the patient on the way out.

The goal is to close a real gap in care: the discharge paperwork patients receive today is often generic, hard to read, and quickly thrown away. PostOpCare AI keeps the writing tailored, the evidence current, and the delivery patient-friendly.

## Highlights

- **Retrieval-augmented generation** over a curated corpus of PubMed abstracts and society guidelines, with BM25 and dense-vector hybrid search.
- **Citation-first writing.** Inline `[^N]` markers map to a numbered source list. The pipeline never invents references.
- **Readability gating.** Every section is scored with Flesch-Kincaid (ease of understanding) before publishing; anything above 9th grade is flagged.
- **Patient-ready delivery.** Each handout gets a stable slug, a public `/h/{slug}` page, a print stylesheet, and a server-rendered QR code.
- **Ten procedures out of the box** spanning Orthopedic, General Surgery, OB/GYN, and Emergency Medicine, with prompt templates for the six sections clinicians actually need (Overview, Pain Management, Activity Restrictions, Wound Care, Warning Signs, and Follow-Up Care).

## How it works

```
Clinician picks procedure
         │
         ▼
┌──────────────────────┐    hybrid search     ┌────────────────────┐
│  Next.js front-end   │ ───────────────────▶ │  Pinecone + BM25   │
│  (App Router, React) │                      │  evidence corpus   │
└──────────┬───────────┘                      └─────────┬──────────┘
           │                                            │
           │ POST /api/generate-handout                 │ top-k chunks
           ▼                                            ▼
┌──────────────────────┐    prompt + context  ┌────────────────────┐
│  FastAPI RAG service │ ───────────────────▶ │  OpenAI (GPT-4o)   │
└──────────┬───────────┘                      └─────────┬──────────┘
           │                                            │
           │ persists Handout, Sections, Citations      │
           ▼                                            ▼
┌──────────────────────┐                      ┌────────────────────┐
│  SQLite (SQLAlchemy) │                      │  Readability gate  │
└──────────┬───────────┘                      └────────────────────┘
           │
           ▼
   /h/{slug} public page  +  /api/handouts/{slug}/qr.png
```

The ingestion side (under `src/backend/ingestion/`) handles PubMed scraping, guideline scraping, and PDF text extraction. Documents are chunked, embedded, and indexed. At request time, `core/rag_pipeline.py` runs the hybrid search, formats a numbered context block, fills in a prompt template from `src/backend/prompts/`, and asks the LLM for a single section. The API endpoint generates all six sections, persists everything, and returns the patient-facing payload.

## Tech stack

**Frontend**
- Next.js 16 (App Router) and React 19
- TypeScript, Tailwind CSS v4, Radix UI primitives, shadcn/ui, lucide-react
- Server-rendered public handout pages with print-optimized styling

**Backend**
- FastAPI and Pydantic v2
- SQLAlchemy 2.0 with SQLite for handout persistence
- Pinecone for dense vector search, `rank_bm25` for lexical search
- OpenAI client for embeddings and generation
- PyMuPDF and pdfplumber for guideline PDF extraction
- `textstat` for readability scoring, `qrcode` for patient share codes, `nanoid` for slug allocation

## Getting started

### Prerequisites

- Node.js 20+ and npm
- Python 3.11+
- An OpenAI API key
- A Pinecone account and index (free tier is fine for development)
- Optionally, an NCBI API key to lift PubMed rate limits from 3 to 10 req/sec

### 1. Clone and install

```bash
git clone https://github.com/<your-org>/postopcare-ai-1.git
cd postopcare-ai-1
npm install
```

### 2. Configure environment

Copy the backend env template and fill in real values:

```bash
cp src/backend/.env.example src/backend/.env
```

The variables you need:

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | yes | Embeddings and section generation |
| `PINECONE_API_KEY` | yes | Vector store auth |
| `PINECONE_INDEX_NAME` | yes | Defaults to `postopcare-rag` |
| `DATABASE_URL` | no | Defaults to `sqlite:///./postopcare.db` |
| `PUBLIC_BASE_URL` | yes | Used to build patient share links and QR codes |
| `NCBI_API_KEY` | no | Higher PubMed rate limit |
| `LOG_LEVEL` | no | Defaults to `INFO` |

### 3. Run the backend

```bash
cd src/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

The API will be live at `http://localhost:8000`. Hit `GET /api/health` to confirm.

### 4. Seed procedures and ingest evidence

From `src/backend` with the venv active:

```bash
python -m db.seed_procedures
python -m ingestion.pubmed_scraper --procedure total-knee-replacement
```

The scrapers populate Pinecone and the local SQLite database so the RAG pipeline has something to retrieve.

### 5. Run the frontend

In a second terminal, from the repo root:

```bash
npm run dev
```

Open `http://localhost:3000`, pick a procedure, and click Generate.

## API reference

All endpoints are JSON unless noted.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Readiness probe. |
| `GET` | `/api/procedures` | List procedures grouped by specialty. |
| `POST` | `/api/generate-section` | Generate a single section for a procedure. |
| `POST` | `/api/generate-handout` | Generate the full six-section handout, persist it, and return a slug, public URL, and QR path. |
| `GET` | `/api/handouts/{slug}` | Fetch a published handout by slug. |
| `GET` | `/api/handouts/{slug}/qr.png` | Server-rendered PNG QR code that points at the public handout URL. |

## Project structure

```
postopcare-ai-1/
├── src/
│   ├── app/                       Next.js App Router
│   │   ├── page.tsx               Clinician workspace
│   │   └── h/[slug]/              Public patient-facing handout view + print
│   ├── components/                React components (handout display, citations, etc.)
│   ├── data/                      Procedure catalog and mock fixtures
│   ├── lib/                       Frontend utilities
│   ├── types/                     Shared TS types
│   └── backend/
│       ├── api/main.py            FastAPI composition root
│       ├── core/                  RAG pipeline, hybrid search, prompts, readability
│       ├── db/                    SQLAlchemy models and seed scripts
│       ├── ingestion/             PubMed, guideline, and PDF ingestion jobs
│       ├── prompts/               Section prompt templates
│       └── tests/                 Backend test suite
├── public/                        Static assets
└── package.json
```

## Design choices worth noting

- **Citations are first-class.** The retrieval layer returns chunks with stable `source_id` values, the LLM is instructed to cite by number only, and the API persists every citation against its source document so the public page can render a real reference list rather than dropped text.
- **Readability is enforced, not hoped for.** The quality metrics returned by `/api/generate-handout` include a Flesch-Kincaid grade level. Anything above 9th grade gets flagged as `safety_check: "flagged"` so the clinician sees it before sharing.
- **Slugs are short and unguessable.** Patient links use a 12-character nanoid alphabet, which is short enough to print on a discharge sheet and large enough to avoid enumeration.
- **The frontend and backend are decoupled.** The Next.js app talks to FastAPI over JSON, which means either side can be deployed independently, and the same API can power a future mobile or EHR-embedded client.

## Roadmap

- Optional translation pass (Spanish first) once the English pipeline is stable
- Clinician edit-and-republish flow with version history
- Procedure-specific evidence freshness checks and re-ingestion jobs
- Optional Postgres deployment recipe for production use

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
