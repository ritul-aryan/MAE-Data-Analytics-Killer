import json
import re
from langchain_core.messages import SystemMessage, HumanMessage
from ai_engine.graph.state import GraphState
from ai_engine.llm_config import llm

def storyteller_node(state: GraphState) -> GraphState:
    """Generates Plotly JSON and plain-English narrative."""
    print("--- [NODE] STORYTELLER: Generating Insights & Visuals ---")

    # 1. Strict Prompt Engineering for JSON Output
    system_prompt = """You are a Principal Data Analyst and UI Architect.
    Given the user's intent and the metadata of the cleaned dataset, your job is to generate:
    1. A valid Plotly JSON configuration dictionary for a relevant chart.
    2. A plain-English analytical summary of the data.

    RULES:
    - Output strictly in valid JSON format matching this exact schema:
    {
        "plotly_config": {"data": [...], "layout": {...}},
        "analytical_summary": "Your plain English summary here."
    }
    - DO NOT include markdown formatting like ```json. Just output the raw JSON string."""

    user_prompt = f"""
    User Intent: {state['user_intent']}

    Cleaned Data Metadata:
    {state['data_metadata']}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    print("    🧠 Prompting Gemini 2.5 Flash for story and chart...")
    response = llm.invoke(messages)

    # 2. Clean and Parse JSON
    output_text = response.content.strip() # type: ignore

    # Fallback to remove backticks if the LLM ignores the rule
    if output_text.startswith("```"):
        output_text = re.sub(r"^```(?:json)?\n|\n```$", "", output_text, flags=re.IGNORECASE).strip()

    try:
        parsed_output = json.loads(output_text)
        plotly_config = parsed_output.get("plotly_config", {})
        analytical_summary = parsed_output.get("analytical_summary", "No summary provided.")
        print("    ✅ Story and visuals generated successfully!")
    except json.JSONDecodeError as e:
        print(f"    ❌ Failed to parse JSON: {e}")
        plotly_config = {"error": "Failed to generate chart"}
        analytical_summary = f"Error parsing LLM output: {output_text}"

    return {
        "plotly_config": plotly_config,
        "analytical_summary": analytical_summary
    } # type: ignore