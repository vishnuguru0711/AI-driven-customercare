from flask import Flask, request, jsonify
import joblib

# Load trained chatbot model
model = joblib.load("chatbot_model.pkl")

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the AI Chatbot API!"

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Predict category
    predicted_category = model.predict([user_message])[0]

    # Hardcoded responses based on predicted category
    responses = {
        "Technical Support": "Let me help you with that technical issue.",
        "Billing Support": "It seems like you have a billing issue. Please check your invoice.",
        "Account Issues": "Are you facing trouble logging in? Let’s fix it!"
    }

    bot_response = responses.get(predicted_category, "I'm not sure, let me transfer you to a human agent.")

    return jsonify({"prediction": predicted_category, "response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
