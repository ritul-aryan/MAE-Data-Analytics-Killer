import pandas as pd
from ai_engine.graph.state import GraphState

def orchestrator_node(state: GraphState) -> GraphState:
    """
    Entry node: Parses the file and extracts lightweight metadata
    to pass into the LangGraph state.
    """
    print("--- [NODE] ORCHESTRATOR: Extracting Metadata ---")
    raw_path = state["raw_file_path"]

    try:
        # Load the raw data (Assuming CSV for Phase 1)
        df = pd.read_csv(raw_path)

        # Create a lightweight string representation for the LLM
        metadata = (
            f"Data Shape: {df.shape}\n\n"
            f"Columns & Data Types:\n{df.dtypes.to_string()}\n\n"
            f"Sample Data (First 5 Rows):\n{df.head().to_markdown()}"
        )
        print("    ✅ Metadata extracted successfully.")

    except Exception as e:
        metadata = f"Error loading file: {str(e)}"
        print(f"    ❌ Error extracting metadata: {str(e)}")

    # We return the updated pieces of the state.
    # LangGraph will automatically merge this with the existing state.
    return {"data_metadata": metadata, "retry_count": 0} # type: ignore