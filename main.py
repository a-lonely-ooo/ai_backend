from flask import Flask, request, jsonify, session
import requests
import uuid

app = Flask(__name__)
app.secret_key = '1234'

BASE_URL = "https://wormai.blackaddon3907.workers.dev/?prompt="

# Chat wise memory system
memory = {}

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    user_msg = data.get('message', '').strip()
    chat_id = data.get('chat_id', str(uuid.uuid4()))  # Get chat_id from request or generate new

    if chat_id not in memory:
        memory[chat_id] = []  # Initialize memory for new chat

    memory[chat_id].append(f"User: {user_msg}")

    # Join chat history
    full_prompt = "\n".join(memory[chat_id]) + "\nAI:"
    full_url = BASE_URL + requests.utils.quote(full_prompt)

    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            data = response.json()
            reply = data.get("response", "No response received").strip()

            memory[chat_id].append(f"AI: {reply}")

            return jsonify({'reply': reply, 'chat_id': chat_id})
        else:
            return jsonify({'reply': "server is busy🫤"}), 500
    except Exception as e:
        return jsonify({'reply': "server is busy🫤 else check your internet🛜"}), 500

@app.route('/clear_memory/<chat_id>', methods=['POST'])
def clear_memory(chat_id):
    if chat_id in memory:
        memory[chat_id] = []
        return jsonify({'status': 'success', 'message': f'Memory cleared for chat {chat_id}.'})
    else:
        return jsonify({'status': 'error', 'message': 'Chat not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
