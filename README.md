# ClearScan

Find plastics in products — scan a barcode, get a microplastic risk score.

## Stack

- **Frontend:** React PWA (Vite) — mobile-optimized, installable
- **Backend:** Flask + PostgreSQL
- **Barcode data:** Open Food Facts API + UPC Item DB fallback
- **Risk scoring:** Claude API (Haiku)

## Setup

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill in your values
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

See `backend/.env.example`.
