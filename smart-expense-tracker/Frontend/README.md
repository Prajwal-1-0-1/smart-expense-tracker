# SpendWise

An AI-powered full stack expense tracker that extracts receipt data using Google Gemini and helps users organize, search, and visualize their expenses.

## Live Demo

spend-wise-brown-iota.vercel.app

---

## Features

* JWT-based user authentication
* Expense CRUD (Create, Read, Update, Delete)
* AI-powered receipt parsing using Google Gemini
* Receipt image upload
* Expense analytics dashboard with charts
* Search, filter, and sort expenses
* Responsive user interface

---

## Tech Stack

### Backend

* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT Authentication
* Google Gemini API

### Frontend

* React (Vite)
* Tailwind CSS
* React Router
* Axios
* Recharts

---

## Project Structure

```text
SpendWise/
├── Backend/
├── Frontend/
└── README.md
```

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-github-username>/SpendWise.git
cd SpendWise
```

### Backend

```bash
cd Backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd Frontend
npm install
npm run dev
```

Before running the project, create the required `.env` files in the `Backend` and `Frontend` directories.

---

## Environment Variables

### Backend (`Backend/.env`)

```env
GEMINI_API_KEY=

DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

### Frontend (`Frontend/.env`)

```env
VITE_API_URL=
```

* Leave `VITE_API_URL` empty for local development.
* Set it to your deployed backend URL for production.

---

## Deployment

| Service           | Platform | URL                                                |
| ----------------- | -------- | -------------------------------------------------- |
| Frontend          | Vercel   | https://spend-wise-l4ntsn9pz-dinnerbone.vercel.app |
| Backend           | Render   | https://spendwise-1gfp.onrender.com                |
| API Documentation | Render   | https://spendwise-1gfp.onrender.com/docs           |

---

## Future Improvements

* Budget tracking and spending limits
* Monthly and yearly expense reports
* Cloud storage for receipt images
* Export expenses to CSV/PDF

---

## Author

**Prajwal Y S**
