from typing import Literal
from langgraph.graph import StateGraph, END
from ai_engine.graph.state import GraphState
from ai_engine.agents.orchestrator import orchestrator_node
from ai_engine.agents.data_janitor import janitor_node
from ai_engine.agents.storyteller import storyteller_node

def janitor_router(state: GraphState) -> Literal["retry", "success", "fail"]:
    """Determines if the Janitor needs to retry, failed completely, or succeeded."""
    error = state.get("execution_error")
    retries = state.get("retry_count", 0)
    MAX_RETRIES = 3

    if error and retries < MAX_RETRIES:
        print(f"    🔄 [ROUTER] Error detected. Initiating self-correcting loop (Retry {retries}/{MAX_RETRIES})...")
        return "retry"
    elif error and retries >= MAX_RETRIES:
        print("    🛑 [ROUTER] Max retries reached. Agent failed to correct the code.")
        return "fail"
    else:
        print("    ➡️ [ROUTER] Execution successful. Routing to Storyteller...")
        return "success"

# 1. Initialize the Graph
workflow = StateGraph(GraphState)

# 2. Add our Agent Nodes
workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("janitor", janitor_node)
workflow.add_node("storyteller", storyteller_node)

# 3. Define the Flow (Edges)
workflow.set_entry_point("orchestrator")
workflow.add_edge("orchestrator", "janitor")

# 4. The Self-Correcting Loop (Conditional Edges)
workflow.add_conditional_edges(
    "janitor",
    janitor_router,
    {
        "retry": "janitor",       # Loop back to fix code
        "success": "storyteller", # Move forward to visual generation
        "fail": END               # Abort graph if too many failures
    }
)

# 5. Finish the graph
workflow.add_edge("storyteller", END)

# 6. Compile the graph into an executable application
app = workflow.compile()