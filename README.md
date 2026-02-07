<div align="center">

# 🧞 SQL-Genie

**Transform natural language into SQL queries instantly using the power of Google Gemini AI.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google AI](https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

</div>

---

## 📖 Project Overview

### The Problem
Non-technical users often need to extract insights from databases but lack SQL knowledge. Traditional solutions require either learning SQL or constant reliance on data teams, creating bottlenecks and delays.

### The Solution
**SQL-Genie** bridges the gap between natural language and structured data. By leveraging Google's Gemini LLM with expertly crafted prompt engineering, users can simply ask questions in plain English (or any language) and receive accurate, executable SQL queries in real-time.

> *"What if anyone could query a database just by asking a question?"*

---

## ✨ Key Features

- 🗣️ **Natural Language Processing** — Ask questions in everyday language
- ⚡ **Real-time SQL Generation** — Instant query creation powered by Gemini AI
- 🎯 **Precision Prompt Engineering** — Expertly designed prompts ensure accurate translations
- 🖥️ **Professional UI** — Clean, modern Streamlit interface with custom styling
- 🔒 **Security-First Design** — Only SELECT queries allowed, preventing destructive operations
- 📊 **Transparent Query Display** — See the generated SQL before execution
- 🚀 **Lightweight Architecture** — No Pandas dependency, pure Python data handling

---

## 🏗️ Architecture Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SQL-GENIE ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐     ┌───────────────────┐     ┌──────────────────┐
    │              │     │                   │     │                  │
    │  USER INPUT  │────▶│  MASTER PROMPT    │────▶│   GEMINI LLM     │
    │  (Natural    │     │  (Schema + Rules  │     │   (AI Engine)    │
    │   Language)  │     │   + Examples)     │     │                  │
    │              │     │                   │     │                  │
    └──────────────┘     └───────────────────┘     └────────┬─────────┘
                                                            │
                                                            ▼
    ┌──────────────┐     ┌───────────────────┐     ┌──────────────────┐
    │              │     │                   │     │                  │
    │   STREAMLIT  │◀────│  RESULT DATA      │◀────│   SQLite DB      │
    │   (UI/Table) │     │  (Python Tuples)  │     │   (Execution)    │
    │              │     │                   │     │                  │
    └──────────────┘     └───────────────────┘     └──────────────────┘
```

### Process Flow

| Step | Component | Description |
|:----:|-----------|-------------|
| 1 | **User Input** | User enters a natural language question |
| 2 | **Master Prompt** | Question is combined with schema context and few-shot examples |
| 3 | **Gemini LLM** | AI processes the prompt and generates a SQL query |
| 4 | **SQL Query** | Raw SQL is extracted and displayed for transparency |
| 5 | **SQLite Execution** | Query runs against the database |
| 6 | **Result Visualization** | Data is rendered in a professional HTML table |

---

## 🎯 Prompt Engineering Highlight

The core technical achievement of this project lies in the **Master Prompt** design. Our prompt includes:

```
✅ Explicit Role Definition — "You are a Senior SQLite Expert"
✅ Complete Schema Documentation — Table structure with data types
✅ Strict Output Constraints — No markdown, no explanations
✅ Security Rules — Only SELECT statements allowed
✅ Few-Shot Examples — 5+ curated examples for pattern learning
```

This approach ensures **consistent, accurate, and secure** SQL generation across diverse user queries.

---

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- Google AI API Key ([Get yours here](https://makersuite.google.com/app/apikey))

### Step-by-Step Setup

```bash
# 1. Clone or navigate to the project directory
cd "text to llm app"

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment file
echo GOOGLE_API_KEY=your_api_key_here > .env

# 5. Initialize the database with sample data
python sql.py

# 6. Launch the application
streamlit run app.py
```

### Requirements File

Create `requirements.txt` with:

```txt
streamlit
google-generativeai
python-dotenv
```

---

## 🚀 Usage

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Sample Questions

Try these natural language queries:

| Question | Generated SQL |
|----------|---------------|
| "Show all students" | `SELECT * FROM STUDENT;` |
| "How many students are there?" | `SELECT COUNT(*) FROM STUDENT;` |
| "List Data Science students" | `SELECT * FROM STUDENT WHERE CLASS = 'Data Science';` |
| "Who has the highest marks?" | `SELECT * FROM STUDENT ORDER BY MARKS DESC LIMIT 1;` |
| "Average marks in section A?" | `SELECT AVG(MARKS) FROM STUDENT WHERE SECTION = 'A';` |

---

## 📋 Database Schema

### Table: `STUDENT`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `NAME` | VARCHAR(22) | Student's full name | "Mustafa" |
| `CLASS` | VARCHAR(22) | Department/Course | "Data Science" |
| `SECTION` | VARCHAR(22) | Class section | "A" |
| `MARKS` | INT | Numerical score | 90 |

### Sample Data

```sql
INSERT INTO STUDENT VALUES ('Mustafa', 'Data Science', 'A', 90);
INSERT INTO STUDENT VALUES ('Ville', 'Data Science', 'B', 100);
INSERT INTO STUDENT VALUES ('Mehmet', 'Data Science', 'A', 85);
INSERT INTO STUDENT VALUES ('Heike', 'DEVOPS', 'A', 50);
INSERT INTO STUDENT VALUES ('Alexi', 'DEVOPS', 'A', 50);
```

---

## 🗺️ Future Roadmap

| Priority | Feature | Status |
|:--------:|---------|:------:|
| 🔴 | PostgreSQL & MySQL Support | Planned |
| 🔴 | Multi-table JOIN Queries | Planned |
| 🟡 | Data Visualization with Plotly | In Progress |
| 🟡 | Query History & Favorites | In Progress |
| 🟢 | CSV/Excel Export | Upcoming |
| 🟢 | Voice Input Support | Upcoming |
| 🟢 | Custom Schema Upload | Upcoming |

---

## 📁 Project Structure

```
text-to-llm-app/
├── app.py              # Main Streamlit application
├── sql.py              # Database initialization script
├── student.db          # SQLite database file
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (API keys)
└── README.md           # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ using Google Gemini AI**

</div>
