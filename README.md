# 🚀 Multi-Agent Ecosystem (MAE) - Data Analytics Automator

## 📌 Overview
This project is a functional MVP (Minimum Viable Product) for a "Zero-Knowledge" Multi-Agent Ecosystem. It is designed to automate the traditional Exploratory Data Analysis (EDA) pipeline. You feed it chaotic, messy data, and the autonomous agents handle the preprocessing, cleaning, and intelligent visualization generation. 

**Note:** This repository represents the basic foundation of the architecture. The core pipeline is successfully up and working, but the ecosystem is actively being perfected, expanded, and optimized!

## 🏗️ Architecture & Tech Stack
To ensure a robust, stateful, and highly customizable workflow, the agent orchestration is powered by **LangGraph**, providing greater architectural control for complex, multi-step reasoning compared to standard out-of-the-box agent frameworks.

* **Agent Orchestration:** LangGraph
* **Backend API:** FastAPI (Python)
* **Frontend UI:** React (JavaScript/TypeScript)

## ✨ Key Features (V1)
* **Zero-Knowledge Execution:** Input a raw dataset, and the ecosystem takes over without requiring manual EDA configuration.
* **Autonomous Data Cleaning:** Dedicated agents identify and resolve missing values, outliers, and data formatting inconsistencies.
* **Intelligent Visualization:** The system autonomously generates contextual graphs based on the cleaned metrics.

## 🚀 Getting Started Locally
1. Clone the repository
2. **Backend setup:** Navigate to the `backend` folder, create and activate a virtual environment, run `pip install -r requirements.txt`, and start the server with `uvicorn main:app --reload`.
3. **Frontend setup:** Navigate to the `frontend` folder, run `npm install`, then `npm start`.
4. Upload the included `Messy_Data.csv` to test the foundational agent workflow!
