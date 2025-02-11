from google import genai
import os
from flask import Flask, jsonify, render_template, request
from google.genai import types
from flask_cors import CORS


gemini_api_key = os.getenv("gemini_api_key")

app = Flask(__name__)
CORS(app)

session_history = {}


def chat_kubernetes(user_query):
    client = genai.Client(api_key=gemini_api_key)
    # sys_instruct = f"""
    # You are the chatbot that answers only Kubernetes documentation-related questions.
    # If the user's query is related to a previous query, use the {session_history.get("last_interaction", "")}
    # from the previous turn.
    # If the user's query is completely unrelated, respond politely that you can only answer Kubernetes questions.
    # """
    sys_instruct = f"""
        You are the chatbot that answers users query that is related to only Kubernetes documentation.
        If the user's query is completely unrelated, respond politely that you can only answer Kubernetes questions.
        """

    chat = client.chats.create(model="gemini-2.0-flash",config=types.GenerateContentConfig(
            system_instruction=sys_instruct, max_output_tokens=500,
            temperature=0.1))
    response = chat.send_message(user_query)
    # Store the last interaction in the dictionary
    last_interaction = f"User: {user_query}\nAssistant: {response}"
    session_history["last_interaction"] = last_interaction

    return response.text


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def query():
    try:
        user_query = request.json['query']
        response = chat_kubernetes(user_query)
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
