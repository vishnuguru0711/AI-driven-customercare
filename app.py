from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load("final_model.pkl")

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the ML Model API!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Check if 'features' key exists
        if "features" not in data:
            return jsonify({"error": "Missing 'features' key in request data"}), 400

        # Convert to NumPy array
        features = np.array(data["features"]).reshape(1, -1)  # Reshape for model input

        # Validate input size
        if features.shape[1] != 49:
            return jsonify({"error": f"Expected 49 features, but got {features.shape[1]}"}), 400

        # Make prediction
        prediction = model.predict(features)

        # Return result as JSON
        return jsonify({"prediction": prediction.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
