from ai_engine.agents.orchestrator import orchestrator_node
from ai_engine.graph.state import GraphState

# 1. Mock the state exactly as it would come from a FastAPI upload
mock_initial_state = GraphState(
    user_intent="Clean this sales data.",
    raw_file_path="data/uploads/messy_sales.csv",
    clean_file_path=None,
    data_metadata=None,
    janitor_code=None,
    execution_error=None,
    retry_count=0,
    plotly_config=None,
    analytical_summary=None
)

# 2. Run the node
new_state = orchestrator_node(mock_initial_state)

# 3. Print the result
print("\n--- EXTRACTED METADATA ---")
print(new_state["data_metadata"])