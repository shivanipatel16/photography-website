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
QUIZ_PHOTOS = os.path.join('static', 'quiz_photos')

app = Flask(__name__)
app.config['STATIC_PHOTOS'] = STATIC_PHOTOS
app.config['INTERACTIVE_PHOTOS'] = INTERACTIVE_PHOTOS
app.config['INTERACTIVE_2_PHOTOS'] = INTERACTIVE_2_PHOTOS
app.config['QUIZ_PHOTOS'] = QUIZ_PHOTOS

# {quiz#: [str: quiz_question, str[]: quiz_options, str: user_answer, 
#          str: answer, str: explanation, str: image_filename int: correct_bool]}
quiz_questions = {
    "1": ["What should the photographer do to address the noise in the image?",
         ["Lower the ISO and make the shutter speed slower.",
          "Lower the aperture and make the shutter speed faster.",
          "Lower the ISO.",
          "Increase the aperture and increase the ISO."],
          "", "0", "", "", -1],
    "2": ["Which options will help decrease the brightness of an image the most?",
         ["Increase the ISO level, make the shutter speed faster, increase the aperture",
          "Decrease the ISO level, make the shutter speed slower, decrease the aperture",
          "Increase the ISO level, make the shutter speed faster, decrease the aperture",
          "Decrease the ISO level, make the shutter speed faster, increase the aperture"],
          "", "3", "", "", -1], # TODO: convert this question to multiple choice
    "3": ["Why is this image blurry?",
         ["Exposure", "Shutter speed", "ISO", "Aperture"],
          "", "1", "", "", -1],
    "4": ["Rhonda took this image on the left with the settings, and she was hoping to retake it to look more like the image on the right. What can Rhonda change to get her desired photograph?",
         ["Lower the aperture", "Zoom in on the flower", 
          "Increase the ISO", "Make the shutter speed faster"],
          "", "0", "", "", -1],
    "5": ["This couple wants to take their engagement portrait outdoors. What do they have to account for in this setting?",
         ["Bright outdoor light, and focus on subjects’ faces",
          "Background clarity and details",
          "Subject motion",
          "Nothing"],
          "", "0", "", "", -1],
    "6": ["The photographer has decided to adjust for sunny, bright  outdoor lighting. What settings should be adjusted to account for those conditions?",
         ["Fast shutter speed + low ISO",
          "Slow shutter speed + low ISO",
          "Slow shutter speed + high ISO",
          "Fast shutter speed + high ISO"],
          "", "0", "", "", -1],
    "7": ["What camera settings did the photographer use to take this picture?",
         ["Fast shutter speed + low ISO",
          "Slow shutter speed + low ISO",
          "Slow shutter speed + high ISO",
          "Fast shutter speed + high ISO"],
          "", "1", "", "", -1],
    "8": ["What setting was changed in the second photo, and what was the effect?",
         ["Aperture; background became more detailed",
          "ISO, background became brighter",
          "Shutter speed; background became more detailed",
          "Nothing"],
          "", "0", "", "", -1],
    "9": ["What should be done to put the Capitol Building in focus?",
         ["Increase ISO",
          "Lower the aperture",
          "Increase the aperture and move the focal point",
          "Increase the shutter speed"],
          "", "2", "", "", -1],
}

# {topic: [str: title, int: visit_timestamp, str[]: topic_sentences, 
#          str[]: image_filenames, int: from_quiz_#]}
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

# {topic: [str: title, int: visit_timestamp, str[]: topic_sentences, 
#          str[]: image_filenames, int: from_quiz_#]]}
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


userscore = 0

question_to_review = -1


def get_interactive_lesson_image(lesson_on, iso=None, f_stop=None, shutter_speed=None):
    # TODO: group -- think about how we are going to say which iso is available, how are we going to round, etc?
    # TODO: shivani
    return "_SVP2779.jpg", iso, f_stop, shutter_speed

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

    # TODO: pass in the photo setting to the frontend (what is the iso, aperture, shutter speed?)
    image1 = "\\" + os.path.join(app.config['STATIC_PHOTOS'], f"{lesson_title}-lesson-1.jpg")
    image2 = "\\" + os.path.join(app.config['STATIC_PHOTOS'], f"{lesson_title}-lesson-2.jpg")
    
    return render_template('lesson_static.html', title=lesson_title, desc=lesson_sentences, info=info_arr, image1=image1, image2=image2)

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
    if question not in quiz_questions.keys():
        return render_template('assessment_start.html')

    info_arr = quiz_questions[question]
    text = info_arr[0]
    [choice1, choice2, choice3, choice4] = info_arr[1]
    currentqnumber = question
    nextqnumber = str(int(question) + 1)
    correct_ans = info_arr[3]
    image = "\\" + os.path.join(app.config['QUIZ_PHOTOS'], f"{question}.jpg")
    print(image)
    data = {
        "nextqnumber": nextqnumber,
        "currentqnumber": currentqnumber,
        "correctanswer": correct_ans,
        "text": text,
        "choice1": choice1,
        "choice2": choice2,
        "choice3": choice3,
        "choice4": choice4,
        "image": image
    }
    return render_template('assessment_question.html', data=data)

@app.route('/update_userscore', methods=['GET', 'POST'])
def update_userscore(correct_tally=None):
    global userscore

    json_data = request.get_json()   
    score_tally = int(json_data)
    # print(json_data)
    userscore = userscore + score_tally 
    # print(f"userscore: {userscore}/{9}")

    return jsonify(userscore = userscore)

@app.route('/review_currquestion', methods=['GET', 'POST'])
def review_currquestion (currq):
    global question_to_review

    json_data = request.get_json()   
    question_to_review= int(json_data)

    return jsonify(question_to_review = question_to_review)


@app.route('/assessment_complete')
def assessment_complete():
    return render_template('assessment_complete.html', userscore=userscore)

if __name__ == '__main__':
    app.run(debug=True)
