# FastAPI Vercel Demo

A minimal FastAPI app deployable to Vercel as a serverless Python function.

## Project Structure

```
├── api/
│   └── index.py       # FastAPI app (Vercel entry point)
├── vercel.json        # Vercel routing config
├── requirements.txt   # Python dependencies
└── .gitignore
```

## Endpoints

| Method | Path               | Description          |
|--------|--------------------|----------------------|
| GET    | `/`                | HTML landing page    |
| GET    | `/health`          | Health check + versions |
| GET    | `/random-quote`    | Random dev quote     |
| POST   | `/echo`            | Echo + reverse message |
| GET    | `/docs`            | Swagger UI           |
| GET    | `/redoc`           | ReDoc UI             |

## Deploy to Vercel

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
gh repo create fastapi-vercel-demo --public --push
```

### 2. Deploy via Vercel CLI

```bash
npm i -g vercel
vercel
```

Or connect your GitHub repo at [vercel.com](https://vercel.com) → **Add New Project**.

## Local Development

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

Then open http://localhost:8000
