# FinanceApp

A personal finance tracker that automatically reads purchase confirmation emails and organizes your spending data in real time.

## What it does

- Connects to your Gmail account via IMAP
- Reads and parses purchase confirmation emails (currently supports Banco Inter)
- Extracts transaction data: date, amount, description, and category
- Stores everything in a local SQLite database
- Exposes a REST API so the frontend can fetch and display your financial data

## Tech Stack

**Backend**
- Python
- FastAPI
- SQLite
- IMAP (Gmail integration)

**Frontend**
- React
- Vite

## Project Structure
FinanceApp/
├── core/
│   └── database.py       # Database logic and queries
├── finance-front/        # React frontend
├── api.py                # FastAPI REST endpoints
├── main.py               # Entry point
└── finance.db            # Local SQLite database

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /transacoes | List transactions by month/year |
| GET | /saldo | Get balance for a given month |
| GET | /resumo | Spending summary by category |
| GET | /categoria | Filter transactions by category |
| POST | /transacoes | Add a transaction manually |
| DELETE | /transacoes/{id} | Delete a transaction |

## How to Run

**Backend**
```bash
pip install fastapi uvicorn
uvicorn api:app --reload
```

**Frontend**
```bash
cd finance-front
npm install
npm run dev
```

API runs on `http://localhost:8000`
Frontend runs on `http://localhost:5174`
API docs available at `http://localhost:8000/docs`

## Status

Alpha 1.0 - functional for personal use. Frontend rebuild (Alpha 2.0) in progress with React.
