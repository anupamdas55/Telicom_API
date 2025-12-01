# from fastapi import FastAPI
# from db_config import get_connection

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Telecom API is running successfully!"}

# @app.get("/telecom_churn")
# def get_telecom_churn():
#     try:
#         conn = get_connection()
#         cur = conn.cursor()
        
#         # Fetch all data from table
#         cur.execute("SELECT * FROM telecom_churn;")
#         rows = cur.fetchall()

#         # Get column names
#         col_names = [desc[0] for desc in cur.description]

#         # Convert to JSON (list of dicts)
#         data = [dict(zip(col_names, row)) for row in rows]

#         cur.close()
#         conn.close()

#         return {
#             "status": "success",
#             "total_rows": len(data),
#             "data": data
#         }

#     except Exception as e:
#         return {"status": "error", "message": str(e)}


from fastapi import FastAPI, Header, HTTPException
from db_config import get_connection
import os

app = FastAPI()

# Load API Key from environment variable OR use fallback
API_KEY = os.getenv("API_KEY", "anupam_telecom_apikey405")

# Function to verify API key
def verify_api_key(key: str):
    if key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


@app.get("/")
def home(x_api_key: str = Header(None)):
    verify_api_key(x_api_key)
    return {"message": "Telecom API is running successfully!"}


@app.get("/telecom_churn")
def get_telecom_churn(x_api_key: str = Header(None)):
    verify_api_key(x_api_key)

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM telecom_churn;")
        rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]

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
