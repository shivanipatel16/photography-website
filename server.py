from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import json
import pprint
import os
import time

STATIC_PHOTOS = os.path.join('static', 'static_photos')
INTERACTIVE_PHOTOS = os.path.join('static', 'interactive_photos')
INTERACTIVE_2_PHOTOS = os.path.join('static', 'interactive_2_photos')


app = Flask(__name__)
app.config['STATIC_PHOTOS'] = STATIC_PHOTOS
app.config['INTERACTIVE_PHOTOS'] = INTERACTIVE_PHOTOS
app.config['INTERACTIVE_2_PHOTOS'] = INTERACTIVE_2_PHOTOS

# {quiz#: [str: user_answer, str: answer, str: explanation]}
quiz_questions = {
    "1": ["", "a", ""],
    "2": ["", "", ""], # TODO: convert this question to multiple choice
    "3": ["", "b", ""],
    "4": ["", "a", ""],
    "5": ["", "a", ""],
    "6": ["", "a", ""],
    "7": ["", "b", ""],
    "8": ["", "a", ""],
    "9": ["", "c", ""],
    "10": ["", "", ""]
}

# {topic: [str: title, int: visit_timestamp, str[]: topic_sentences, str[]: image_filenames]}
static_lesson_info = {
    "iso": ["iso", -1, 
           ["Let's say you are ready to take a photo.",
            "You should always assess the light by considering the weather, artificial light, and shadows.",
            "ISO helps you adjust for the light by simply allowing you to brighten or darken the photo."],
           [], -1],
    "aperture": ["aperture", -1,
           ["Aperture also known as “f-stop” controls how sharp the background is.",
           "Now, the background of an image is defined by the focal point (what the camera is set to focus on)"],
           [], -1],
    "shutter_speed": ["shutter_speed", -1,
           ["Shutter speed is the speed at which the shutter of the camera closes.",
           "The longer the shutter speed, the more light strikes the sensor.",
           "A slow shutter speed can be used to capture motion (like image on the left).",
           "1/60 sec is the most common shutter speed for a typical photo."],
           [], -1]
}

# {topic: [str: title, int: visit_timestamp, str[]: topic_sentences, str[]: image_filenames]}
interactive_lesson_info = {
    "iso": ["iso", -1, [], [], -1],
    "aperture": ["aperture", -1, [], [], -1],
    "shutter_speed": ["shutter_speed", -1, [], [], -1]
}

# {topic: [str: title, int: visit_timestamp, str[]: topic_sentences, 
#          str[]: image_filenames, int: from_quiz_#]}
interactive_2_lesson_info = {
    "iso-aperture": ["iso-aperture", -1, [], [], -1],
    "iso-shutter_speed": ["iso-shutter_speed", -1, [], [], -1],
    "aperture-shutter_speed": ["aperture-shutter_speed", -1, [], [], -1]
}

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
    if lesson_topic not in ("iso", "aperture", "shutter_speed"):
        return render_template('home.html')
    
    info_arr = static_lesson_info[lesson_topic]
    lesson_title = info_arr[0]
    info_arr[1] = time.time() # timestamp visit
    lesson_sentences = info_arr[2]

    # copy back over info arr to dictionary
    static_lesson_info[lesson_topic] = info_arr
    print(static_lesson_info[lesson_topic])

    return render_template('lesson_static.html', title=lesson_title, desc=lesson_sentences, info=info_arr)

# /lesson/interactive/iso
# /lesson/interactive/aperture
# /lesson/interactive/shutter_speed
@app.route('/lesson/interactive/<lesson_topic>')
def interactive_lesson(lesson_topic):
    if lesson_topic not in ("iso", "aperture", "shutter_speed"):
        return render_template('home.html')
    
    info_arr = interactive_lesson_info[lesson_topic]
    lesson_title = info_arr[0]
    info_arr[1] = time.time() # timestamp visit
    lesson_sentences = info_arr[2]
    lesson_images = info_arr[3]

    # copy back over info arr to dictionary
    interactive_lesson_info[lesson_topic] = info_arr
    return render_template('lesson_interactive.html', title=lesson_title, desc=lesson_sentences, images=lesson_images, info=info_arr)

# /lesson/interactive/iso/aperture
# /lesson/interactive/iso/shutter_speed
# /lesson/interactive/aperture/shutter_speed
@app.route('/lesson/interactive/<lesson_topic1>/<lesson_topic2>')
def interactive_lesson_2(lesson_topic1, lesson_topic2):
    lesson_topic = '-'.join([lesson_topic1, lesson_topic2])
    if lesson_topic not in ("iso-aperture", "iso-shutter_speed", "aperture-shutter_speed"):
        return render_template('home.html')
    
    info_arr = interactive_2_lesson_info[lesson_topic]
    lesson_title = info_arr[0]
    info_arr[1] = time.time() # timestamp visit
    lesson_sentences = info_arr[2]
    lesson_images = info_arr[3]

    # copy back over info arr to dictionary
    interactive_2_lesson_info[lesson_topic] = info_arr
    print(interactive_2_lesson_info[lesson_topic])
    return render_template('lesson_interactive_2.html', title=lesson_title, desc=lesson_sentences, images=lesson_images, info=info_arr)

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
