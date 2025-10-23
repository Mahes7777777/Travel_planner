import os
from dotenv import load_dotenv
import streamlit as st
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq

# -----------------------
# Initialize LLM
# -----------------------


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.01
)

# -----------------------
# Define LangGraph Nodes
# -----------------------
def get_travel_input(state):
    state["travel_input"] = {
        "destination": st.session_state.get("destination", "Zurich"),
        "area": st.session_state.get("area", "Zurich"),
        "duration_days": st.session_state.get("duration_days", 7),
        "budget": st.session_state.get("budget", 250000),
        "travel_type": st.session_state.get("travel_type", "budget"),
        "interests": st.session_state.get("interests", ["sightseeing", "local food"])
    }
    return state

def analyze_travel_profile(state):
    t = state["travel_input"]
    prompt = f"""
    Analyze user preferences:
    - Destination: {t['destination']} ({t['area']})
    - Duration: {t['duration_days']} days
    - Budget: ₹{t['budget']}
    - Travel type: {t['travel_type']}
    - Interests: {', '.join(t['interests'])}

    Give a short summary and any constraints.
    """
    state["travel_summary"] = llm.predict(prompt)
    return state

def suggest_hotels(state):
    t = state["travel_input"]
    prompt = f"""
    Recommend 2 budget-friendly hotels in {t['area']}, {t['destination']}
    for {t['duration_days']} days under ₹{t['budget']}.

    Include name, price/night, total cost, and reason.
    """
    state["hotel_options"] = llm.predict(prompt)
    return state

def suggest_places(state):
    t = state["travel_input"]
    prompt = f"""
    Suggest 5 must-visit places near {t['destination']} focusing on:
    - Interests: {', '.join(t['interests'])}
    - Travel type: {t['travel_type']}
    - Within 10-15 km of {t['area']}

    Include name and reason to visit.
    """
    state["places_to_visit"] = llm.predict(prompt)
    return state

def cost_estimator(state):
    prompt = f"""
    Estimate total travel cost for {state['travel_input']['duration_days']}-day trip to {state['travel_input']['destination']}:
    - Hotel: {state['hotel_options']}
    - Places: {state['places_to_visit']}
    Break down: Hotel, Transport, Food, Entry, Misc
    Include total cost and check if within ₹{state['travel_input']['budget']}
    """
    state["cost_estimate"] = llm.predict(prompt)
    return state

def travel_summary(state):
    summary = f"""
**Travel Summary:** {state['travel_summary']}

**Hotel Options:** {state['hotel_options']}

**Places to Visit:** {state['places_to_visit']}

**Cost Estimate:** {state['cost_estimate']}
"""
    state["summary"] = summary
    return state

# -----------------------
# Build LangGraph
# -----------------------
graph = StateGraph(dict)
graph.add_node("input", get_travel_input)
graph.add_node("analyze", analyze_travel_profile)
graph.add_node("hotels", suggest_hotels)
graph.add_node("places", suggest_places)
graph.add_node("cost", cost_estimator)
graph.add_node("summary", travel_summary)

graph.set_entry_point("input")
graph.add_edge("input", "analyze")
graph.add_edge("analyze", "hotels")
graph.add_edge("hotels", "places")
graph.add_edge("places", "cost")
graph.add_edge("cost", "summary")
graph.set_finish_point("summary")
graph.compile()

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="LangGraph Traveller Agent", layout="wide")
st.title("LangGraph Traveller Agent")

# Travel Input Form
with st.form("travel_form"):
    st.subheader("Enter Travel Details")
    st.text_input("Destination", key="destination", value="")
    st.text_input("Area / Locality", key="area", value="")
    st.number_input("Duration (days)", key="duration_days", max_value=30, value=0)
    st.number_input("Budget (₹)", key="budget", min_value=1000, step=1000)
    st.selectbox("Travel Type", key="travel_type", options=["budget", "standard", "luxury"])
    st.multiselect(
        "Interests",
        key="interests",
        options=["sightseeing", "local food", "shopping", "history", "adventure"],
        default=["sightseeing", "local food"]
    )
    submitted = st.form_submit_button("Generate Travel Plan")

# Run LangGraph and show results
if submitted:
    st.info("Generating travel plan...")
    try:
        # Step 1: Compile the graph
        compiled_graph = graph.compile()
        
        # Step 2: Invoke the compiled graph
        result = compiled_graph.invoke({})  # invoke works on compiled graph only
        
        st.success("Travel Plan Generated!")
        st.markdown(result["summary"])
    except Exception as e:
        st.error(f"Failed to generate travel plan: {e}")

