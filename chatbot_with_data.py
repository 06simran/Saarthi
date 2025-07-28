import json

# Load mission data from JSON
def load_mission_data(path="data/isro_missions.json"):
    with open(path, "r") as f:
        return json.load(f)

# Match mission in question
def find_mission_by_name(question, missions):
    q_clean = question.lower().replace("-", "").replace(" ", "")
    for m in missions:
        m_clean = m["mission"].lower().replace("-", "").replace(" ", "")
        if m_clean in q_clean:
            return m
    return None

# Basic logic
def answer_question(missions, question):

    mission_data = find_mission_by_name(question, missions)

    if not mission_data:
        return "🤖 Sorry, I couldn't find any matching mission."

    q_lower = question.lower()

    if "when" in q_lower or "date" in q_lower or "launched" in q_lower:
        if mission_data.get("launch_info"):
            return f"🚀 {mission_data['mission']} was launched: {mission_data['launch_info']}"
        else:
            return f"🤖 Launch date for {mission_data['mission']} is not available."

    elif "what is" in q_lower or "tell me" in q_lower or "about" in q_lower:
        return f"🛰️ {mission_data['mission']}: {mission_data['description']}"

    return f"🤖 Saarthi is not sure what you're asking about {mission_data['mission']}."

# Main loop
if __name__ == "__main__":
    missions = load_mission_data()
    print("🤖 Saarthi is ready with mission data! (type 'exit' to quit)")

    while True:
        q = input("🧑 You: ")
        if q.lower() in ["exit", "quit", "bye"]:
            print("👋 Saarthi: Goodbye!")
            break
        print("🤖 Saarthi:", answer_question(missions, q))
