from ai_engine.graph.workflow import app

# 1. Define the initial payload (What FastAPI will eventually send)
initial_payload = {
    "user_intent": "Clean this sales data. Drop rows where 'Amount' is invalid. Fill missing 'Customer_Name' with 'Unknown'. Show me a bar chart of the sales amounts by customer.",
    "raw_file_path": "data/uploads/messy_sales.csv",
    "clean_file_path": None,
    "data_metadata": None,
    "janitor_code": None,
    "execution_error": None,
    "retry_count": 0,
    "plotly_config": None,
    "analytical_summary": None
}

print("\n🚀 [STARTING LANGGRAPH WORKFLOW]")

# 2. Invoke the compiled graph
# This single line runs the Orchestrator -> Janitor -> (Loop if needed) -> Storyteller
final_state = app.invoke(initial_payload) # type: ignore

print("\n🎉 [WORKFLOW COMPLETE]")
print("\n=== FINAL ANALYTICAL SUMMARY ===")
print(final_state["analytical_summary"])