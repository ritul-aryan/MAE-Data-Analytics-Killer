from ai_engine.agents.orchestrator import orchestrator_node
from ai_engine.agents.data_janitor import janitor_node
from ai_engine.agents.storyteller import storyteller_node
from ai_engine.graph.state import GraphState
import json

# 1. Define the initial state
state = GraphState(
    user_intent="Clean this sales data. Drop rows where 'Amount' is invalid. Fill missing 'Customer_Name' with 'Unknown'. Show me a bar chart of the sales amounts by customer.",
    raw_file_path="data/uploads/messy_sales.csv",
    clean_file_path=None,
    data_metadata=None,
    janitor_code=None,
    execution_error=None,
    retry_count=0,
    plotly_config=None,
    analytical_summary=None
)

# 2. Run the full pipeline!
print("\n[STARTING FULL PIPELINE TEST]")
state.update(orchestrator_node(state))
state.update(janitor_node(state))
state.update(storyteller_node(state))

# 3. Print the Final Outputs
print("\n=== FINAL ANALYTICAL SUMMARY ===")
print(state["analytical_summary"])

print("\n=== PLOTLY JSON CONFIGURATION ===")
print(json.dumps(state["plotly_config"], indent=2))