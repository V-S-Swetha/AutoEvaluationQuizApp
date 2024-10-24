import csv
import os
from flask import Flask, render_template, request, redirect, url_for
from questions import questions

app = Flask(__name__)

# Define the file path for storing results
results_file = 'results/student_results.csv'

# Ensure the results directory exists
if not os.path.exists('results'):
    os.makedirs('results')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_quiz():
    user_name = request.form.get('name')
    if not user_name:
        return redirect(url_for('index'))
    return redirect(url_for('quiz', user_name=user_name))

@app.route('/quiz/<user_name>', methods=['GET', 'POST'])
def quiz(user_name):
    if request.method == 'POST':
        score = 0
        user_answers = {}
        for q in questions:
            user_answer = request.form.get(q['question'])
            user_answers[q['question']] = user_answer
            if user_answer == q['answer']:
                score += 1
        
        # Save results to CSV
        with open(results_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_name, score, user_answers])

        return redirect(url_for('result', user_name=user_name, score=score))
    return render_template('quiz.html', user_name=user_name, questions=questions)

@app.route('/result/<user_name>/<int:score>')
def result(user_name, score):
    total_questions = len(questions)
    return render_template('result.html', user_name=user_name, score=score, total_questions=total_questions)

@app.route('/results')
def view_results():
    with open(results_file, mode='r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return render_template('view_results.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
