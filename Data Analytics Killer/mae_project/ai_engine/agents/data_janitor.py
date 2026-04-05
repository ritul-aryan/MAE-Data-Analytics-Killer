import re
import pandas as pd
from langchain_core.messages import SystemMessage, HumanMessage
from ai_engine.graph.state import GraphState
from ai_engine.llm_config import llm

def extract_python_code(text: str) -> str:
    """Extracts python code from markdown blocks if the LLM includes them."""
    # The regex pattern looks for markdown code blocks and extracts the content inside
    pattern = r"```(?:python)?\n(.*?)```"

    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()

def janitor_node(state: GraphState) -> GraphState:
    """Generates Pandas cleaning code via Gemini and executes it."""
    print(f"--- [NODE] DATA JANITOR (Attempt {state.get('retry_count', 0) + 1}) ---")

    raw_path = state["raw_file_path"]
    # Create the destination path by swapping the folder name
    clean_path = raw_path.replace("uploads", "processed")

    # 1. Strict Prompt Engineering
    system_prompt = """You are a Principal Data Engineer.
    Your job is to write pure, executable Python Pandas code to clean a messy dataset based on the user's intent.

    RULES:
    1. Output ONLY the raw Python code. Do not include markdown formatting or explanations.
    2. Read the file from the pre-defined variable: `raw_path`.
    3. Save the cleaned DataFrame to the pre-defined variable: `clean_path` using `df.to_csv(clean_path, index=False)`.
    4. Assume `import pandas as pd`, `raw_path`, and `clean_path` are already available in the environment.
    5. DO NOT wrap the code in a function. Write a direct script.
    6. CRITICAL: NEVER use `inplace=True`. Modern Pandas blocks this. Always reassign the variable (e.g., `df['col'] = df['col'].fillna('val')`)."""

    user_prompt = f"""
    User Intent: {state['user_intent']}

    Data Metadata:
    {state['data_metadata']}

    Previous Execution Error (if you are retrying): {state.get('execution_error', 'None')}
    """

    # 2. Call Gemini 2.5 Pro
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    print("    🧠 Prompting Gemini 2.5 Pro for cleaning code...")
    response = llm.invoke(messages)

    # 3. Extract Code
    executable_code = extract_python_code(response.content) # type: ignore

    # 4. Execute Code (Local Sandbox)
    error_msg = None
    new_metadata = state["data_metadata"]

    # These variables are injected directly into the execution environment
    local_vars = {
        "pd": pd,
        "raw_path": raw_path,
        "clean_path": clean_path
    }

    try:
        print("    ⚙️ Executing generated code...")
        # WARNING: exec() is fine for local prototyping.
        # In a real SaaS, this must run in an isolated Docker container or E2B sandbox.
        exec(executable_code, globals(), local_vars)

        # If execution succeeds, update the metadata for the Storyteller node
        clean_df = pd.read_csv(clean_path)
        new_metadata = (
            f"Cleaned Data Shape: {clean_df.shape}\n\n"
            f"Cleaned Columns & Types:\n{clean_df.dtypes.to_string()}\n\n"
            f"Cleaned Sample Data:\n{clean_df.head().to_markdown()}"
        )
        print("    ✅ Data cleaned successfully!")

    except Exception as e:
        error_msg = str(e)
        print(f"    ❌ Execution failed: {error_msg}")

    return {
        "janitor_code": executable_code,
        "execution_error": error_msg,
        "retry_count": state.get("retry_count", 0) + 1,
        "clean_file_path": clean_path if not error_msg else None,
        "data_metadata": new_metadata
    } # type: ignore