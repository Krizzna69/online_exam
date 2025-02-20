from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory, jsonify
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuration
IMAGE_DIR = os.path.join('static', 'images')
DEFAULT_START_TIME = "2025-02-20 05:24:14"
DEFAULT_USER = "Krizzna69"

# Ensure the images directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Decorator to check if exam is terminated
def check_termination(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('exam_terminated') and request.endpoint not in ['exam_terminated', 'admin']:
            return redirect(url_for('exam_terminated'))
        return f(*args, **kwargs)
    return decorated_function

# Your existing questions list remains the same

questions = [
    {
        "id": 1,
        "java_image": "java_q1.png",
        "c_image": "c_q1.png",
        "python_image": "python_q1.png",
        "test_cases": [
            {
                "input": "nums = [2,7,11,15], target = 9",
                "expected_output": "[0,1]"
            },
            {
                "input": "nums = [3,2,4], target = 6",
                "expected_output": "[1,2]"
            },
            {
                "input": "nums = [3,3], target = 6",
                "expected_output": "[0,1]"
            }
        ],
        "description": "Find the bug in the code that calculates the sum of first n natural numbers and also solve the two sum problem.",
        "correct_answer": "i+1"
    },
    {
        "id": 2,
        "java_image": "java_q2.png",
        "c_image": "c_q2.png",
        "python_image": "python_q2.png",
        "test_cases": [
            {
                "input": "LinkedList: 1->2->3->4->5",
                "expected_output": "3 (middle element)"
            },
            {
                "input": "LinkedList: 1->2->3->4->5->6",
                "expected_output": "4 (second middle element for even length)"
            },
            {
                "input": "LinkedList: 1",
                "expected_output": "1 (single element)"
            }
        ],
        "description": "Find the bug in the code that finds the middle node of a linked list. The code should handle both odd and even length lists. For even length, it should return the second middle element. Each language has the same logical error in the while loop condition. Fix the condition based on the language syntax.",
       "correct_answer": "return -1"
    },
    {
        "id": 3,
        "java_image": "java_q3.png",
        "c_image": "c_q3.png",
        "python_image": "python_q3.png",
        "test_cases": [
            {
                "input": "root = [1,2,3]",
                "expected_output": "6"
            },
            {
                "input": "root = [-10,9,20,null,null,15,7]",
                "expected_output": "42"
            }
        ],
        "description": "Find the bug in the code that calculates the maximum path sum of a binary tree.",
        "correct_answer": "return 0"
    },
    {
        "id": 4,
        "java_image": "java_q4.png",
        "c_image": "c_q4.png",
        "python_image": "python_q4.png",
        "test_cases": [
            {
                "input": "boxes = [1,3,2,2,2,3,4,3,1]",
                "expected_output": "23"
            },
            {
                "input": "boxes = [1,1,1]",
                "expected_output": "9"
            },
            {
                "input": "boxes = [1]",
                "expected_output": "1"
            }
        ],
        "description": "Find the bug in the code that calculates the maximum points that can be obtained by removing boxes with the given algorithm.",
        "correct_answer": "m"
    },
    {
        "id": 5,
        "description": "Find the galaxy and stars within them from a given 3xN matrix of characters { #, *, . }.",
        "test_cases": [
            {
                "input": "18\n* . * # * * * # * * * # * * * . * .\n* . * # * . * # . * . # * * * * * *\n* * * # * * * # * * * # * * * * . *",
                "expected_output": "U#O#I#EA"
            }
        ],
        'correct_answer' : 'i=0',
    }
]


@app.route('/')
@check_termination
def index():
    session.clear()
    session['current_question'] = 1
    session['start_time'] = DEFAULT_START_TIME
    session['user'] = DEFAULT_USER
    return redirect(url_for('question', question_id=1))

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
@check_termination
def question(question_id):
    if 'current_question' not in session:
        return redirect(url_for('index'))

    question = next((q for q in questions if q['id'] == question_id), None)
    if not question:
        return "Invalid Question ID."

    if request.method == 'POST':
        user_output = request.form.get('user_output', '').strip().lower()
        
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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        admin_pass = data.get('admin_password')
        
        if admin_pass == 'jaswanthkrishna2817':  # In production, use secure password handling
            if action == 'reset_all':
                session.clear()
                return jsonify({
                    'status': 'success',
                    'message': 'All exams reset successfully',
                    'timestamp': DEFAULT_START_TIME
                })
            elif action == 'view_status':
                return jsonify({
                    'status': 'success',
                    'active_sessions': len(session),
                    'terminated_exams': session.get('terminated_count', 0),
                    'last_reset': session.get('last_reset', 'Never'),
                    'timestamp': DEFAULT_START_TIME
                })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid admin password',
                'timestamp': DEFAULT_START_TIME
            })
    
    return render_template('admin.html',
                         current_user=DEFAULT_USER,
                         current_date=DEFAULT_START_TIME)

@app.route('/static/images/<path:filename>')
@check_termination
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

@app.route('/exam_terminated', methods=['GET', 'POST'])
def exam_terminated():
    session['exam_terminated'] = True
    session['terminated_count'] = session.get('terminated_count', 0) + 1
    return render_template('exam_terminated.html',
                         current_user=DEFAULT_USER,
                         current_date=DEFAULT_START_TIME)

@app.route('/congratulations')
@check_termination
def congratulations():
    return render_template('congratulations.html',
                         current_user=DEFAULT_USER,
                         current_date=DEFAULT_START_TIME)

if __name__ == '__main__':
    app.run(debug=True)