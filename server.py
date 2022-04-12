from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import json
import pprint

app = Flask(__name__)

def get_static_lesson_image(lesson_on):
    # TODO: shivani
    images = ["_SVP2779.jpg", "f / 1.4", "_SVP2779.jpg", "f / 3.9"]

def get_interactive_lesson_image(lesson_on, iso=None, f_stop=None, shutter_speed=None):
    # TODO: group -- think about how we are going to say which iso is available, how are we going to round, etc?
    # TODO: shivani
    return "_SVP2779.jpg", iso, f_stop, shutter_speed

def get_quiz_image(question_number):
    # TODO: shivani
    return "_SVP2779.jpg"

@app.route('/')
def welcome():
    return render_template('home.html')

@app.route('/lesson')
def lesson():
    return render_template('lesson.html')

# /lesson/iso
# /lesson/aperture
# /lesson/shutter_speed
@app.route('/lesson/<lesson_topic>')
def static_lesson(lesson_topic):
    return render_template('lesson_static.html')

# /lesson/interactive/iso
# /lesson/interactive/aperture
# /lesson/interactive/shutter_speed
@app.route('/lesson/interactive/<lesson_topic>')
def interactive_lesson(lesson_topic):
    return render_template('lesson_interactive.html')

# /lesson/interactive/iso/aperture
# /lesson/interactive/iso/aperture
# /lesson/interactive/aperture/shutter_speed
@app.route('/lesson/interactive/<lesson_topic1>/<lesson_topic2>')
def interactive_lesson_2(lesson_topic1, lesson_topic2):
    return render_template('lesson_interactive_2.html')

@app.route('/assessment_start')
def assessment_start():
    return render_template('assessment_start.html')

@app.route('/assessment/<question>')
def assessment_question(question):
    return render_template('assessment_question.html', data=question)

@app.route('/assessment_complete')
def assessment_complete():
    return render_template('assessment_complete.html')

if __name__ == '__main__':
    app.run(debug=True)
