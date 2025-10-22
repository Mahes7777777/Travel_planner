🧳 Traveller Agent — Streamlit App

An AI-powered travel planner built using Streamlit, LangGraph, and ChatGroq LLM.
It generates personalized travel itineraries based on user preferences like destination, budget, duration, and interests.

🚀 Features

🗺️ Custom travel itinerary generation using LangGraph flow

💰 Smart cost estimation and budget breakdown

🧠 LLM-powered responses via ChatGroq (Llama model)

🎨 Clean and interactive Streamlit UI

⚙️ Mock fallback when no API key is provided

🧩 LangGraph Practice Flow

This project also serves as practice for building agent workflows using LangGraph.
It demonstrates how to design state-based AI pipelines step by step.

🧠 Flow Explanation

Here’s how the LangGraph workflow operates:

User Input Node — collects user preferences (destination, budget, duration, etc.)

Travel Planning Node — uses LLM (ChatGroq) to generate itinerary ideas

Cost Estimation Node — calculates estimated trip cost based on inputs

Summary Node — summarizes the plan with day-wise details and insights

End Node — returns the complete travel plan and cost breakdown

Each node represents a function connected in a LangGraph state machine — showing how data (“state”) flows through steps just like a real AI agent.


Folder Structure:
traveller_agent/
│
├── app/
│   ├── __init__.py
│   ├── streamlit_travel_app.py      # 👉 main Streamlit UI
│   ├── travel_logic.py              # 👉 core travel logic functions
│   └── utils.py                     # 👉 helper utilities (prompt builders, text cleaners)
│
├── data/                            # 👉 optional saved travel data or configs
├── requirements.txt
└── README.md



How to run:

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app/streamlit_travel_app.py



















