from typing import TypedDict, Optional, Dict, Any

class GraphState(TypedDict):
    """
    The state payload passed between nodes.
    We pass file paths and metadata string representations, NOT raw DataFrames.
    """
    user_intent: str
    raw_file_path: str
    clean_file_path: Optional[str]

    # Lightweight context for the LLM
    data_metadata: Optional[str]

    # Janitor Execution State
    janitor_code: Optional[str]
    execution_error: Optional[str]
    retry_count: int

    # Storyteller Output
    plotly_config: Optional[Dict[str, Any]]
    analytical_summary: Optional[str]