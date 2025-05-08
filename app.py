from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import datetime
import os

app = Flask(__name__)

# Set your Gemini API key here
genai.configure(api_key="your-api-key-here")  # Replace with actual API key

chat_history = []

# Initialize the model
model = genai.GenerativeModel("gemini-pro")
chat_session = model.start_chat(history=[])

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history, chat_session

    if request.method == "POST":
        user_input = request.form["user_input"]
        chat_history.append({"sender": "user", "text": user_input})

        try:
            response = chat_session.send_message(user_input)
            bot_reply = response.text.strip()
        except Exception as e:
            print(f"[ERROR] Gemini API failed: {e}")  # 👈 Print the actual error to terminal
            bot_reply = "I'm here for you! Let's keep talking, even if I'm having a hiccup with my AI brain."

        chat_history.append({"sender": "vars", "text": bot_reply})
        return redirect(url_for("index"))

    # Greet the user when first loaded
    if not chat_history:
        greeting = "Hello! I'm VARS, your AI companion. How can I help you today?"
        chat_history.append({"sender": "vars", "text": greeting})

    return render_template("index.html", messages=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
