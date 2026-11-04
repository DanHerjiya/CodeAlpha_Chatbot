
from datetime import datetime
import random
import re
import ast
import operator

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Supported mathematical operations
OPERATIONS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod
}


# Safely calculate simple mathematical expressions
def calculate(expression):
    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value

            if isinstance(node, ast.BinOp):
                operation = OPERATIONS.get(type(node.op))

                if operation:
                    return operation(
                        evaluate(node.left),
                        evaluate(node.right)
                    )

            raise ValueError("Invalid calculation")

        return evaluate(tree)

    except Exception:
        return None


# Generate chatbot responses
def get_bot_response(message):

    text = message.strip().lower()

    if not text:
        return "Please type a message."

    # Greetings
    if re.search(
        r"\b(hello|hi|hey|good morning|good afternoon|good evening)\b",
        text
    ):
        return (
            "Hello! Welcome to Classic Chatbot. "
            "How can I help you today?"
        )

    # Chatbot identity
    if "your name" in text or "who are you" in text:
        return (
            "I am Classic Chatbot, your simple virtual assistant. "
            "I am here to answer your questions and help you."
        )

    # Help
    if "help" in text or "what can you do" in text:
        return (
            "Here are some things I can do:\n"
            "1. Respond to greetings.\n"
            "2. Explain Python and Flask.\n"
            "3. Tell you the date and time.\n"
            "4. Share motivational quotes.\n"
            "5. Calculate simple mathematics.\n"
            "6. Answer some general questions."
        )

    # Time
    if "time" in text:
        return (
            "The current server time is "
            + datetime.now().strftime("%I:%M %p")
        )

    # Date
    if "date" in text or "today" in text:
        return (
            "Today's date is "
            + datetime.now().strftime("%d %B %Y")
        )

    # Motivational messages
    if any(word in text for word in [
        "motivation",
        "motivate me",
        "inspire me",
        "encourage me"
    ]):
        quotes = [
            "Great things are achieved through small, consistent steps.",
            "Every expert was once a beginner. Keep learning.",
            "Progress is more important than perfection.",
            "Believe in yourself and never give up on your dreams.",
            "Your future is created by what you do today.",
            "Success comes to those who remain determined and hardworking."
        ]

        return random.choice(quotes)

    # Python explanation
    if "python" in text:
        return (
            "Python is a popular programming language used "
            "for web development, automation, artificial intelligence "
            "and data analysis."
        )

    # Flask explanation
    if "flask" in text:
        return (
            "Flask is a lightweight Python web framework "
            "used to build websites and web applications."
        )

    # Cloud computing explanation
    if "cloud computing" in text:
        return (
            "Cloud computing means using computing services "
            "such as storage, servers and applications over the internet."
        )

    # Computer explanation
    if "computer" in text:
        return (
            "A computer is an electronic device that accepts data, "
            "processes it, stores it and produces information."
        )

    # Internet explanation
    if "internet" in text:
        return (
            "The internet is a global network that connects computers "
            "and devices, allowing people to share information."
        )

    # Artificial intelligence explanation
    if "artificial intelligence" in text or text == "what is ai":
        return (
            "Artificial Intelligence, or AI, is technology that enables "
            "computers to perform tasks that normally require human "
            "intelligence, such as understanding language and solving problems."
        )

    # Mathematics
    match = re.search(
        r"(-?\d+(?:\.\d+)?\s*[+\-*/%]\s*-?\d+(?:\.\d+)?)",
        text
    )

    if match:
        answer = calculate(match.group(1))

        if answer is not None:
            return f"The answer is {answer}."

        return "I could not calculate that expression."

    # Thank you
    if "thank you" in text or "thanks" in text:
        return "You're welcome! I'm happy to help you."

    # Goodbye
    if "bye" in text or "goodbye" in text:
        return (
            "Goodbye! Thank you for chatting with Classic Chatbot. "
            "Have a wonderful day!"
        )

    # Default response
    return (
        "I'm sorry, I don't have an answer for that question yet. "
        "Please type 'help' to see what I can do."
    )


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "")

    if not isinstance(message, str):
        return jsonify({
            "reply": "Please enter a text message."
        }), 400

    if len(message) > 500:
        return jsonify({
            "reply": "Please keep your message under 500 characters."
        }), 400

    response = get_bot_response(message)

    return jsonify({
        "reply": response
    })


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
