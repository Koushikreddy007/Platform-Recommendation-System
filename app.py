from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load and prepare the dataset
df = pd.read_csv("expanded_social_media_knowledge_dataset.csv")

# Label encode categorical columns
le_occupation = LabelEncoder()
le_purpose = LabelEncoder()
le_platform = LabelEncoder()

df["Occupation_encoded"] = le_occupation.fit_transform(df["Occupation"])
df["Primary_Purpose_encoded"] = le_purpose.fit_transform(df["Primary_Purpose"])
df["Platform_Used_encoded"] = le_platform.fit_transform(df["Platform_Used"])

# Features and target
X = df[["Age", "Occupation_encoded", "Usage_Per_Day (hrs)", "Primary_Purpose_encoded"]]
y = df["Platform_Used_encoded"]

# Train the model
model = DecisionTreeClassifier()
model.fit(X, y)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    age = data.get("age")
    occupation = data.get("occupation")
    usage = data.get("usage_per_day")
    purpose = data.get("purpose")

    try:
        occ_encoded = le_occupation.transform([occupation])[0]
        pur_encoded = le_purpose.transform([purpose])[0]
    except:
        return jsonify({"error": "Invalid occupation or purpose"}), 400

    input_df = pd.DataFrame([{
        "Age": age,
        "Occupation_encoded": occ_encoded,
        "Usage_Per_Day (hrs)": usage,
        "Primary_Purpose_encoded": pur_encoded
    }])

    pred_encoded = model.predict(input_df)[0]
    platform = le_platform.inverse_transform([pred_encoded])[0]

    return jsonify({"recommended_platform": platform})

if __name__ == "__main__":
    app.run(debug=True)
