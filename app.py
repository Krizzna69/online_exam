from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuration
IMAGE_DIR = os.path.join('static', 'images')

# Ensure the images directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Sample questions with image filenames
questions = [
    {
        "id": 1,
        "java_image": "java_q1.png",
        "c_image": "c_q1.png",
        "python_image": "python_q1.png",
        "test_cases": [
            {
                "input": "5",
                "expected_output": "15"
            },
            {
                "input": "3",
                "expected_output": "6"
            },
            {
                "input": "0",
                "expected_output": "0"
            }
        ],
        "description": "Find the bug in the code that calculates the sum of first n natural numbers.",
        "correct_answer": "n+1"
    },
    {
        "id": 2,
        "java_image": "java_q2.png",
        "c_image": "c_q2.png",
        "python_image": "python_q2.png",
        "test_cases": [
            {
                "input": "s = '()[]{}'" ,
                "expected_output": "true"
            },
            {
                "input": "s = \"(]\"",
                "expected_output": "false"
            },
            {
                "input": "s = \"([])\"",
                "expected_output": "true"
            }
        ],
        "description": "Find the bug in the Valid Parentheses code. The code should validate if the string contains valid parentheses pairs.",
        "correct_answer": "}"
    }
]
@app.route('/')
def index():
    session['current_question'] = 1
    session['start_time'] = "2025-02-19 15:59:24"  # Updated timestamp
    session['user'] = "Krizzna69"
    return redirect(url_for('question', question_id=1))

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    if 'current_question' not in session:
        session['current_question'] = 1

    question = next((q for q in questions if q['id'] == question_id), None)
    if not question:
        return "Invalid Question ID."

    if request.method == 'POST':
        user_output = request.form.get('user_output', '').strip().lower()
        
        # Check if the answer matches the correct answer
        if user_output == question['correct_answer'].lower():
            session['current_question'] += 1
            if session['current_question'] > len(questions):
                return redirect(url_for('congratulations'))
            else:
                return redirect(url_for('question', question_id=session['current_question']))
        else:
            error = "Incorrect! Please try again."
            return render_template('question.html',
                               question_id=question_id,
                               question=question,
                               error=error,
                               current_user=session['user'],
                               current_date=session['start_time'])

    return render_template('question.html',
                       question_id=question_id,
                       question=question,
                       current_user=session['user'],
                       current_date=session['start_time'])

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

@app.route('/congratulations')
def congratulations():
    return "<h1>Congratulations! You have completed the exam! 🎉</h1>"

@app.route('/exam_terminated')
def exam_terminated():
    return "<h1>Exam Terminated - Tab switching detected</h1><p>Your exam has been terminated because you switched tabs/windows.</p>"

if __name__ == '__main__':
    app.run(debug=True)