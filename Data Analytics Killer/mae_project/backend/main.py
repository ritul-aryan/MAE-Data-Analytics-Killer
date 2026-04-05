import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai_engine.graph.workflow import app as langgraph_app

# Initialize FastAPI
app = FastAPI(title="Data Analytics Killer API", version="1.0.0")

# Allow React to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/analyze")
async def analyze_data(intent: str = Form(...), file: UploadFile = File(...)):
    """
    Receives a CSV file and a user intent, saves the file temporarily,
    and passes it through the LangGraph Multi-Agent Ecosystem.
    """
    print(f"\n🌐 [API] Received request: '{intent}' with file: {file.filename}")

    # 1. Save the uploaded file with a unique ID to prevent overlapping requests
    file_extension = file.filename.split('.')[-1] # type: ignore
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"    💾 [API] File saved to {file_path}")

        # 2. Build the initial Graph State
        initial_payload = {
            "user_intent": intent,
            "raw_file_path": file_path,
            "clean_file_path": None,
            "data_metadata": None,
            "janitor_code": None,
            "execution_error": None,
            "retry_count": 0,
            "plotly_config": None,
            "analytical_summary": None
        }

        # 3. Run the LangGraph Engine!
        print("    🚀 [API] Triggering LangGraph Workflow...")
        final_state = langgraph_app.invoke(initial_payload) # type: ignore

        # 4. Return the exact payload the React frontend needs
        return {
            "status": "success",
            "analytical_summary": final_state.get("analytical_summary"),
            "plotly_config": final_state.get("plotly_config"),
            "clean_file_path": final_state.get("clean_file_path")
        }

    except Exception as e:
        print(f"    ❌ [API] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))