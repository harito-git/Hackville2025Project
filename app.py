import os
from flask import Flask, request, render_template_string, session, redirect, url_for, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Check if the API key was successfully loaded
if not GEMINI_API_KEY:
    raise ValueError("Google Gemini API Key not found. Please ensure it's set in the .env file.")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')  # Secret key for sessions

# HTML template with Tailwind styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat with Gemini</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-800">
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Chat with Google Gemini</h1>
        
        {% if not cookie_accepted %}
        <div class="p-4 bg-yellow-200 text-gray-800 mb-4">
            <p>We use cookies to enhance your experience. Do you accept?</p>
            <form method="POST" action="/accept_cookies">
                <button type="submit" name="choice" value="accept" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Accept Cookies</button>
                <button type="submit" name="choice" value="deny" class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 ml-2">Deny Cookies</button>
            </form>
        </div>
        {% endif %}
        
        <form method="POST" class="mb-4">
            <textarea name="user_input" class="w-full p-2 border border-gray-300 rounded mb-2" rows="4" placeholder="Type your message here..."></textarea>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Send</button>
        </form>

        {% if response %}
        <div class="p-4 bg-white shadow rounded">
            <strong>Gemini:</strong>
            <p>{{ response }}</p>
        </div>
        {% endif %}
        
        <!-- Generate Workout Form -->
        <div class="container mx-auto p-4">
            <h1 class="text-2xl font-bold mb-4">Generate Your Personalized Gym Workout Plan</h1>
            <form id="workout-form" class="mb-4">
                <textarea
                    id="workout-input"
                    class="w-full p-2 border border-gray-300 rounded mb-2"
                    rows="4"
                    placeholder="Type your fitness preferences here..."
                ></textarea>
                <button
                    type="submit"
                    class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                    Generate Workout Plan
                </button>
            </form>

            <div id="workout-result" class="p-4 bg-white shadow rounded hidden">
                <h2 class="text-xl font-bold">Your Personalized Workout Plan:</h2>
                <p id="workout-text"></p>
            </div>

            <div id="workout-error" class="p-4 bg-red-200 rounded hidden">
                <p id="error-text" class="text-red-600"></p>
            </div>
        </div>

    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def chat_page():
    cookie_accepted = session.get('cookie_accepted', None)
    response = None

    if request.method == 'POST' and request.form.get('user_input'):
        user_input = request.form.get('user_input')

        # Generate content using user input
        try:
            start_time = time.time()

            gemini_response = model.generate_content(user_input)

            elapsed_time = time.time() - start_time
            if elapsed_time > 30:
                response = f"Response took too long ({elapsed_time:.2f} seconds). Please try again."
            else:
                response = gemini_response.text

        except Exception as e:
            response = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, response=response, cookie_accepted=cookie_accepted)

@app.route('/accept_cookies', methods=['POST'])
def accept_cookies():
    choice = request.form.get('choice')
    if choice == 'accept':
        session['cookie_accepted'] = True  # Store cookie acceptance in session
    elif choice == 'deny':
        session['cookie_accepted'] = False  # Store cookie denial in session
    return redirect(url_for('chat_page'))  # Redirect back to the main chat page

@app.route('/api/generate_workout', methods=['POST'])
def generate_workout():
    data = request.get_json()
    user_input = data.get("user_input")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        gemini_response = model.generate_content(f"Create a personalized gym workout plan for the following: {user_input}")
        workout_plan = gemini_response.text
        return jsonify({"workout_plan": workout_plan}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # For local development using self-signed certificate
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
