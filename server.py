from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import json
import pprint
import re
import natsort
import os
import time

app = Flask(__name__)

# Server configuration

## Configure server filepaths
STATIC_PHOTOS = os.path.join('static', 'static_photos')
INTERACTIVE_PHOTOS = os.path.join('static', 'interactive_photos')
INTERACTIVE_2_PHOTOS = os.path.join('static', 'interactive_2_photos')
QUIZ_PHOTOS = os.path.join('static', 'quiz_photos')

app.config['STATIC_PHOTOS'] = STATIC_PHOTOS
app.config['INTERACTIVE_PHOTOS'] = INTERACTIVE_PHOTOS
app.config['INTERACTIVE_2_PHOTOS'] = INTERACTIVE_2_PHOTOS
app.config['QUIZ_PHOTOS'] = QUIZ_PHOTOS

## Helper functions to retrieve image filepaths
def get_interactive_images(lesson):
    filenames = list()
    for file in os.listdir(app.config['INTERACTIVE_PHOTOS']):
        if file.startswith(lesson):
            f = "\\" + os.path.join(app.config['INTERACTIVE_PHOTOS'], file)
            setting = re.search(r'-(.*?).jpg', file).group(1)
            if "~" in setting:
                setting = setting.replace("~", "/", 1)

            filenames.append((f, setting))
    sorted_filenames = natsort.natsorted(filenames)

    if lesson == "shutter_speed":
        sorted_filenames = sorted_filenames[:5][::-1] + sorted_filenames[5:]

    return sorted_filenames


def get_static_filenames(lesson):
    filenames = list()
    for file in os.listdir(app.config['STATIC_PHOTOS']):
        if file.startswith(lesson):
            filenames.append("\\" + os.path.join(app.config['STATIC_PHOTOS'], file))
    return natsort.natsorted(filenames)


# Server Data
## Global Variables
userscore = 0
question_to_review = -1

# {quiz#: [str: quiz_question, str[]: quiz_options, str: user_answer,
#          str: answer, str: explanation, str: image_filename int: correct_bool]}
quiz_questions = {
    "1": ["What should the photographer do to address the noise in the image?",
          ["Lower the ISO and make the shutter speed slower.",
           "Lower the aperture and make the shutter speed faster.",
           "Lower the ISO.",
           "Increase the aperture and increase the ISO."],
          "", 
          "0", 
          "Noise occurs when the ISO is too high. In order to compensate a lower ISO, you must allow the image to become brighter either by making the shutter speed slower or lowering the aperture.", # quiz_questions[4] str: explanation
          "", -1],
    "2": ["Which options will help decrease the brightness of an image the most?",
          ["Increase the ISO level, make the shutter speed faster, increase the aperture",
           "Decrease the ISO level, make the shutter speed slower, decrease the aperture",
           "Increase the ISO level, make the shutter speed faster, decrease the aperture",
           "Decrease the ISO level, make the shutter speed faster, increase the aperture"],
          "",
          "3", 
          "The higher the ISO, the brighter the image. The slower the shutter speed, the more light that the camera lets in. The lower the aperture, the brighter the background.", # quiz_questions[4] str: explanation 
          "", -1], 
    "3": ["Why is this image blurry?",
          ["Exposure", "Shutter Speed", "ISO", "Aperture"],
          "", 
          "1", 
          "This image is blurry because the shutter speed was so slow that the image captured the movement of the person holding the camera.", # quiz_questions[4] str: explanation 
          "", -1],
    "4": [
        "Rhonda took this image on the left with the settings, and she was hoping to retake it to look more like the image on the right. What can Rhonda change to get her desired photograph?",
        ["Lower the aperture", "Zoom in on the flower",
         "Increase the ISO", "Make the shutter speed faster"],
        "", 
        "0", 
        "The difference between the two images is the background blur. In order lower the clarity on the background, the aperture should be lowered.", # quiz_questions[4] str: explanation 
        "", -1],
    "5": [
        "This couple wants to take their engagement portrait outdoors. What do they have to account for in this setting?",
        ["Bright outdoor light, and focus on subjects’ faces",
         "Background clarity and details",
         "Subject motion",
         "Nothing"],
        "", 
        "0", 
        "In order to put lots of emphasis on the couple, we must make sure the focus is on their faces. Furthermore, the lighting conditions affect the settings of the images greatly since sunny lighting is already very bright.", # quiz_questions[4] str: explanation 
        "", -1],
    "6": [
        "The photographer has decided to adjust for sunny, bright outdoor lighting. What settings should be adjusted to account for those conditions?",
        ["Fast shutter speed + low ISO",
         "Slow shutter speed + low ISO",
         "Slow shutter speed + high ISO",
         "Fast shutter speed + high ISO"],
        "", 
        "0", 
        "In order to account for bright outdoor lighting, you must have a low ISO. A fast shutter speed means less light enters the camera, which means the photo will not be overly bright.", # quiz_questions[4] str: explanation 
        "", -1],
    "7": ["What camera settings did the photographer use to take this picture?",
          ["Fast shutter speed + low ISO",
           "Slow shutter speed + low ISO",
           "Slow shutter speed + high ISO",
           "Fast shutter speed + high ISO"],
          "", 
          "1", 
          "In order to capture the light trails, the shutter speed must be very slow (30 seconds). Because of such a slow shutter speed, the ISO must be very low so that the photo is not overly bright.", # quiz_questions[4] str: explanation 
          "", -1],
    "8": ["What setting was changed in the second photo, and what was the effect?",
          ["Aperture; background became more detailed",
           "ISO, background became brighter",
           "Shutter speed; background became more detailed",
           "Nothing"],
          "", 
          "0", 
          "The background became more details and in focus which is controlled by aperture. A higher aperture (f-stop) increases the focus on the background details of an image.", # quiz_questions[4] str: explanation 
          "", -1],
    "9": ["What should be done to put the Capitol Building in focus?",
          ["Increase ISO",
           "Lower the aperture",
           "Increase the aperture or move the focal point",
           "Increase the shutter speed"],
          "", 
          "2", 
          "Remember that background clarity is controlled by aperture. Furthermore, moving the focal point of the image can put the building in the foreground instead of the background.", # quiz_questions[4] str: explanation 
          "", -1],
}

# {topic: [str: title, int: visit_timestamp, str[]: topic_sentences, 
#          str[]: image_filenames, int: from_quiz_#, str[]: image_settings]}
static_lesson_info = {
    "iso": ["Iso", -1,
            ["Let's say you are ready to take a photo.",
             "You should always assess the light by considering the weather, artificial light, and shadows.",
             "ISO helps you adjust for the light by simply allowing you to brighten or darken the photo.", "If the ISO is too high, then there will be noise in the photo."],
            get_static_filenames("iso"), -1, ["ISO 7200", "ISO 500"]],
    "aperture": ["Aperture", -1,
                 ["Aperture also known as “f-stop” controls how sharp the background is.",
                  "Now, the background of an image is defined by the focal point (what the camera is set to focus on)"],
                 get_static_filenames("aperture"), -1, ["f / 7.3", "f / 4.0"]],
    "shutter_speed": ["Shutter Speed", -1,
                      ["Shutter speed is the speed at which the shutter of the camera closes.",
                       "The longer the shutter speed, the more light strikes the sensor.",
                       "A slow shutter speed can be used to capture motion (like image on the left).",
                       "1/60 sec is the most common shutter speed for a typical photo."],
                      get_static_filenames("shutter_speed"), -1, ["1/2000 sec", "2 sec"]]
}

# {topic: [str: title, int: visit_timestamp, str[]: topic_sentences, 
#          str[]: image_filenames, int: from_quiz_#]]}
interactive_lesson_info = {
    "iso": ["Iso", -1, [], get_interactive_images("iso"), -1],
    "aperture": ["Aperture", -1, [], get_interactive_images("aperture"), -1],
    "shutter_speed": ["Shutter Speed", -1, [], get_interactive_images("shutter_speed"), -1]
}

# {topic: [str: title, int: visit_timestamp, str[]: topic_sentences, 
#          str[]: image_filenames, int: from_quiz_#]}
interactive_2_lesson_info = {
    "iso-aperture": ["iso-aperture", -1, [], [], -1],
    "iso-shutter_speed": ["iso-shutter_speed", -1, [], [], -1],
    "aperture-shutter_speed": ["aperture-shutter_speed", -1, [], [], -1]
}

@app.route('/')
def welcome():
    return render_template('home.html')


@app.route('/lesson')
def lesson():
    iso_visit = static_lesson_info["iso"][1]
    spd_visit = static_lesson_info["shutter_speed"][1]
    ape_visit = static_lesson_info["aperture"][1]
    return render_template('lesson.html', iso_visit=iso_visit, spd_visit=spd_visit, 
                            ape_visit=ape_visit, question_to_review=question_to_review)


# /lesson/iso
# /lesson/aperture
# /lesson/shutter_speed
@app.route('/lesson/<lesson_topic>')
def static_lesson(lesson_topic):
    if lesson_topic not in ("iso", "aperture", "shutter_speed"):
        return render_template('home.html')

    info_arr = static_lesson_info[lesson_topic]
    lesson_title = info_arr[0]
    lesson_topic = lesson_topic
    info_arr[1] = time.time()  # timestamp visit
    lesson_sentences = info_arr[2]
    lesson_images = info_arr[3]
    lesson_settings = info_arr[5]
    # copy back over info arr to dictionary
    static_lesson_info[lesson_topic] = info_arr
    print(static_lesson_info[lesson_topic])

    return render_template('lesson_static.html', title=lesson_title, lesson_topic=lesson_topic, desc=lesson_sentences, info=info_arr,
                           image1=lesson_images[0], image2=lesson_images[1], setting1=lesson_settings[0], setting2=lesson_settings[1])


# /lesson/interactive/iso
# /lesson/interactive/aperture
# /lesson/interactive/shutter_speed
@app.route('/lesson/interactive/<lesson_topic>')
def interactive_lesson(lesson_topic):
    if lesson_topic not in ("iso", "aperture", "shutter_speed"):
        return render_template('home.html')

    print(static_lesson_info[lesson_topic][1]) # timestamp
    info_arr = interactive_lesson_info[lesson_topic]
    print(info_arr)
    lesson_title = info_arr[0]
    lesson_topic = lesson_topic
    info_arr[1] = time.time()  # timestamp visit
    lesson_sentences = info_arr[2]
    lesson_images = info_arr[3]

    # copy back over info arr to dictionary
    interactive_lesson_info[lesson_topic] = info_arr
    return render_template('lesson_interactive.html', title=lesson_title, lesson_topic=lesson_topic, desc=lesson_sentences, 
                            images=lesson_images, num_images=len(lesson_images), info=info_arr)


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
    info_arr[1] = time.time()  # timestamp visit
    lesson_sentences = info_arr[2]
    lesson_images = info_arr[3]
    # copy back over info arr to dictionary
    interactive_2_lesson_info[lesson_topic] = info_arr
    print(interactive_2_lesson_info[lesson_topic])
    print(lesson_images)
    return render_template('lesson_interactive_2.html', title=lesson_title, desc=lesson_sentences, images=lesson_images,
                           info=info_arr)


@app.route('/assessment_start')
def assessment_start():
    return render_template('assessment_start.html', question_to_review=question_to_review)


@app.route('/assessment/<question>')
def assessment_question(question):
    if question not in quiz_questions.keys():
        return render_template('assessment_start.html')

    info_arr = quiz_questions[question]
    text = info_arr[0]
    [choice0, choice1, choice2, choice3] = info_arr[1]
    currentqnumber = question
    nextqnumber = str(int(question) + 1)
    correct_ans = info_arr[3]
    explanation_text = info_arr[4]
    image = "\\" + os.path.join(app.config['QUIZ_PHOTOS'], f"{question}.jpg")
    print(image)
    data = {
        "nextqnumber": nextqnumber,
        "currentqnumber": currentqnumber,
        "correctanswer": correct_ans,
        "text": text,
        "choice0": choice0,
        "choice1": choice1,
        "choice2": choice2,
        "choice3": choice3,
        "image": image,
        "explanation_text": explanation_text
    }
    return render_template('assessment_question.html', data=data)


@app.route('/update_userscore', methods=['GET', 'POST'])
def update_userscore(correct_tally=None):
    global userscore

    json_data = request.get_json()
    score_tally = int(json_data)
    print(json_data)
    userscore = userscore + score_tally
    print(f"userscore: {userscore}/{9}")

    return jsonify(userscore=userscore)


@app.route('/review_currquestion', methods=['GET', 'POST'])
def review_currquestion():
    global question_to_review

    json_data = request.get_json()
    question_to_review = int(json_data)
    print(question_to_review)

    return jsonify(question_to_review=question_to_review)


@app.route('/assessment_complete')
def assessment_complete():
    global userscore
    global question_to_review

    score = userscore
    userscore = 0 # reset stored userscore
    question_to_review = -1

    return render_template('assessment_complete.html', userscore=score)


if __name__ == '__main__':
    app.run(debug=True)
