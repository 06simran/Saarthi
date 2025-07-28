import networkx as nx
import json
from knowledge_graph import build_knowledge_graph
from nlp_engine import extract_entities

# Load ISRO updates
def load_updates(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Answer the user's question using graph and basic NLP
def answer_question(graph, question):
    doc_entities = extract_entities([question])[0]["entities"]

    mission = None
    intent = None

    # Step 1: Try detecting mission from entities
    for ent, label in doc_entities:
        if label == "PRODUCT":
            mission = ent

    # Step 2: Fallback to keyword match if spaCy missed mission
    if not mission:
        mission_nodes = [n for n, attr in graph.nodes(data=True) if attr.get("label") == "PRODUCT"]
        q_clean = question.lower().replace("-", "").replace(" ", "")
        for m in mission_nodes:
            m_clean = m.lower().replace("-", "").replace(" ", "")
            if m_clean in q_clean:
                mission = m
                break

    # Step 3: Detect intent from question text
    q_lower = question.lower()
    if "when" in q_lower or "date" in q_lower or "launched" in q_lower:
        intent = "date_query"
    elif "what is" in q_lower or "tell me" in q_lower or "about" in q_lower or "information" in q_lower:
        intent = "info_query"

    # Debug output
    print(f"🎯 Detected mission: {mission}, intent: {intent}")

    # Step 4: Answer based on intent
    if mission and intent == "date_query":
        for neighbor in graph.neighbors(mission):
            if graph[mission][neighbor]["relation"] == "launch_date":
                return f"{mission} was launched on {neighbor}."
        return f"Sorry, I couldn't find the launch date for {mission}."

    elif mission and intent == "info_query":
        return f"{mission} is one of ISRO's key missions. More information will be available soon."

    return "🤖 I'm still learning. Can you rephrase your question?"

# Main chatbot loop
if __name__ == "__main__":
    data = load_updates("data/isro_updates.json")
    entities = extract_entities(data)
    G = build_knowledge_graph(entities)

    print("🤖 Saarthi is ready. Ask me about ISRO missions! (type 'exit' to quit)")
    print("📊 Known missions:", [n for n, a in G.nodes(data=True) if a.get("label") == "PRODUCT"])

    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Saarthi: Goodbye!")
            break
        response = answer_question(G, user_input)
        print("🤖 Saarthi:", response)
