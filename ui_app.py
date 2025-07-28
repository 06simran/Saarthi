from flask import Flask, render_template, request, jsonify
from chatbot_with_data import answer_question as get_response, load_mission_data

app = Flask(__name__)

# Load mission data once at startup
missions = load_mission_data()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    reply = get_response(missions, user_msg)  # ✅ Pass both args
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
