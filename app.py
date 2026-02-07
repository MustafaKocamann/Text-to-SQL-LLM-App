"""
Text-to-SQL Application
A lightweight Streamlit app that converts natural language to SQL queries
using Groq AI. No Pandas - uses native Python data structures.
"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
from groq import Groq

# ============================================================
# CONFIGURATION
# ============================================================

# Configure Groq API
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Database path
DATABASE_PATH = "student.db"

# ============================================================
# CUSTOM CSS STYLING
# ============================================================

def inject_custom_css():
    """Inject custom CSS for professional styling."""
    st.markdown("""
    <style>
        /* Remove top padding from main container */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2rem;
        }
        
        .main-header p {
            color: rgba(255,255,255,0.9);
            margin: 0.5rem 0 0 0;
        }
        
        /* Custom table styling */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 0.95rem;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        
        .custom-table thead tr {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: left;
            font-weight: 600;
        }
        
        .custom-table th,
        .custom-table td {
            padding: 12px 15px;
        }
        
        .custom-table tbody tr {
            border-bottom: 1px solid #dddddd;
            background-color: #ffffff;
            color: #333333;
        }
        
        .custom-table td {
            color: #333333 !important;
        }
        
        .custom-table tbody tr:nth-of-type(even) {
            background-color: #f9f9f9;
        }
        
        .custom-table tbody tr:last-of-type {
            border-bottom: 2px solid #667eea;
        }
        
        .custom-table tbody tr:hover {
            background-color: #f1f1f1;
        }
        
        /* SQL code block styling */
        .sql-section {
            background: #1e1e1e;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Results section */
        .results-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Input styling */
        .stTextInput > div > div > input {
            border-radius: 8px;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# LLM FUNCTIONS
# ============================================================

def get_groq_response(question: str, prompt: str) -> str:
    """
    Send question and prompt to Groq and get the SQL query response.
    
    Args:
        question: User's natural language question
        prompt: System prompt with database schema and instructions
        
    Returns:
        Generated SQL query as string
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=500
    )
    
    # Clean the response - remove any markdown formatting
    sql_query = chat_completion.choices[0].message.content.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    return sql_query


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def execute_sql_query(sql: str, db_path: str) -> tuple:
    """
    Execute SQL query and return results with column headers.
    Uses native Python - no Pandas!
    
    Args:
        sql: SQL query to execute
        db_path: Path to SQLite database
        
    Returns:
        Tuple of (column_names, rows) where:
        - column_names: List of column name strings
        - rows: List of tuples containing row data
        
    Raises:
        sqlite3.Error: If query execution fails
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql)
        
        # Extract column names from cursor.description
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        # Fetch all rows as list of tuples
        rows = cursor.fetchall()
        
        return column_names, rows
        
    finally:
        conn.close()


def render_html_table(columns: list, rows: list) -> str:
    """
    Render data as a styled HTML table.
    
    Args:
        columns: List of column header names
        rows: List of tuples containing row data
        
    Returns:
        HTML string for the styled table
    """
    if not columns or not rows:
        return ""
    
    # Build table header
    header_html = "".join(f"<th>{col}</th>" for col in columns)
    
    # Build table rows
    rows_html = ""
    for row in rows:
        cells = "".join(f"<td>{cell}</td>" for cell in row)
        rows_html += f"<tr>{cells}</tr>"
    
    # Combine into full table
    table_html = f"""
    <table class="custom-table">
        <thead>
            <tr>{header_html}</tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
    
    return table_html


# ============================================================
# PROMPT TEMPLATE
# ============================================================

SYSTEM_PROMPT = """
### ROLE
You are a Senior SQLite Expert and Data Analyst. Your mission is to translate natural language questions into highly accurate, executable SQL queries for a specific database.

### DATABASE SCHEMA
Table: STUDENT
Columns: 
- NAME (VARCHAR): The full name of the student.
- CLASS (VARCHAR): The department or course name (e.g., 'Data Science', 'DEVOPS').
- SECTION (VARCHAR): The class section or group (e.g., 'A', 'B').
- MARKS (INT): The numerical score or grade of the student.

### CONSTRAINTS & RULES
1. OUTPUT FORMAT: Return ONLY the raw SQL code. 
2. NO MARKDOWN: Do not use code blocks (```sql), do not use the word "sql", and do not provide explanations.
3. CASE SENSITIVITY: For string filtering (WHERE clause), use the LIKE operator with '%' for flexible matching if the user is imprecise, or exact strings if clear.
4. SYNTAX: Use standard SQLite syntax.
5. SECURITY: Only generate SELECT statements. Do not allow DROP, DELETE, or UPDATE commands.

### FEW-SHOT EXAMPLES
Example 1 - User: "How many student records are there?"
Query: SELECT COUNT(*) FROM STUDENT;

Example 2 - User: "Show students in the Data Science class."
Query: SELECT * FROM STUDENT WHERE CLASS = 'Data Science';

Example 3 - User: "Who are the top 3 students by marks?"
Query: SELECT NAME, MARKS FROM STUDENT ORDER BY MARKS DESC LIMIT 3;

Example 4 - User: "What is the average mark in section A?"
Query: SELECT AVG(MARKS) FROM STUDENT WHERE SECTION = 'A';

Example 5 - User: "List all students and their details."
Query: SELECT * FROM STUDENT;

### TASK
Based on the rules above, convert the following user question into a SQL query:
"""


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    """Main application entry point."""
    
    # Page configuration
    st.set_page_config(
        page_title="Text to SQL | Groq AI",
        page_icon="🔍",
        layout="centered"
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Text to SQL Generator</h1>
        <p>Transform natural language into SQL queries using Groq AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User input section
    st.markdown("### 💬 Ask Your Question")
    question = st.text_input(
        label="Enter your question",
        placeholder="e.g., Show all students in Data Science class",
        label_visibility="collapsed"
    )
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit = st.button("🚀 Generate Query", use_container_width=True)
    
    # Process query when submitted
    if submit and question:
        with st.spinner("🔄 Generating SQL query..."):
            try:
                # Get SQL from Groq
                generated_sql = get_groq_response(question, SYSTEM_PROMPT)
                
                # Display the generated SQL
                st.markdown("---")
                st.markdown("### 📝 Generated SQL Query")
                st.code(generated_sql, language="sql")
                
                # Execute the query
                try:
                    columns, rows = execute_sql_query(generated_sql, DATABASE_PATH)
                    
                    # Results section
                    st.markdown("### 📊 Query Results")
                    
                    if rows:
                        # Show row count
                        st.success(f"✅ Found {len(rows)} record(s)")
                        
                        # Render results as HTML table
                        table_html = render_html_table(columns, rows)
                        st.markdown(table_html, unsafe_allow_html=True)
                        
                    else:
                        st.warning("⚠️ No data found for this query.")
                        
                except sqlite3.Error as db_error:
                    st.error(f"❌ Database Error: {str(db_error)}")
                    st.info("💡 Tip: Make sure the query syntax is correct and the table exists.")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Please check your API key and try again.")
    
    elif submit and not question:
        st.warning("⚠️ Please enter a question first.")
    
    # Footer with instructions
    st.markdown("---")
    with st.expander("📖 How to use this app"):
        st.markdown("""
        1. **Enter your question** in natural language (e.g., "Show all students with marks above 80")
        2. **Click 'Generate Query'** to create the SQL
        3. **View the results** in the table below
        
        **Example questions:**
        - "How many students are there?"
        - "Show students in Data Science class"
        - "Who has the highest marks?"
        - "List all students in section A"
        - "What is the average marks?"
        """)


if __name__ == "__main__":
    main()