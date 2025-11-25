from fastapi import FastAPI
from db_config import get_connection

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Telecom API is running successfully!"}

@app.get("/telecom_churn")
def get_telecom_churn():
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Fetch all data from table
        cur.execute("SELECT * FROM telecom_churn;")
        rows = cur.fetchall()

        # Get column names
        col_names = [desc[0] for desc in cur.description]

        # Convert to JSON (list of dicts)
        data = [dict(zip(col_names, row)) for row in rows]

        cur.close()
        conn.close()

        return {
            "status": "success",
            "total_rows": len(data),
            "data": data
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
