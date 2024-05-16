from flask import Flask, render_template, jsonify, session, url_for
from flask_socketio import SocketIO
import pandas as pd
import random
import serial
import content_class


try:
    ser = serial.Serial('/dev/cu.usbmodemHIDPC1', 9600, timeout=1)
    print("PORT SUCCESS")
except:
    print("PORT NOT FOUND")
import random
previous_numbers_f = set()
previous_numbers_r = set()
def generate_unique_random_f():
    global previous_numbers_f
    while True:
        num = random.randint(0, 198)
        if num not in previous_numbers_f:
            previous_numbers_f.add(num)
            return num

def generate_unique_random_r():
    global previous_numbers_r
    while True:
        num = random.randint(0, 198)
        if num not in previous_numbers_r:
            previous_numbers_r.add(num)
            return num

round_count = 0
total_qs = 0

img_l = []
img_r = []

for i in range(200):
    if i!=0:
        img_l.append("f"+str(i)+".jpg")
        img_r.append("r" + str(i) + ".jpg")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)




fake_data = pd.read_csv('gpt_combined.csv', header=None)
# Extract the first column (index 0) and convert it to a list
fake_list= fake_data[0].tolist()

real_data = pd.read_csv('real_combined.csv', header=None)
# Extract the first column (index 0) and convert it to a list
real_list= real_data[0].tolist()

first_text = fake_list[0]
right_text = real_list[0]
right_answer_count = 0

def calculate_score(right_answers):
    score_ = int((right_answers/15)*100)
    print('from function ra', right_answers)
    if score_ >80:
        score_ = random.randint(75, 85)
    #value = random.randint(60, 90)
    return score_


@app.route('/index')
def index():
    global total_qs,  round_count, previous_numbers_f,previous_numbers_r, right_answer_count
    total_qs = 0
    right_answer_count = 0
    round_count = 0
    previous_numbers_f = set()
    previous_numbers_r = set()
    print(previous_numbers_f, previous_numbers_r)

    print("hello world index page loaded, variables set to 0")
    df = pd.read_csv('images.csv')  # Assuming your CSV file is named 'data.csv'
    #first_image_url = df.iloc[0,0] # Assuming 'image_url' is the column containing image URLs
    first_image_url = img_l[0]
    first_right_image = img_r[0]
    #return render_template('index.html', first_image_url=first_image_url)

    first_text = fake_list[0]
    right_text = real_list[0]

    return render_template('index.html', first_image_url=first_image_url,  first_string=first_text, right_image_url=first_right_image, right_string=right_text)



@app.route('/next')
def next_file():
    global first_image_url, first_text, list_headlines,total_qs,round_count,img_l,im_r,right_answer_count
    total_qs += 1
    print('left clicked, total_qs:', total_qs)
    print('hellogg', right_answer_count)
    if total_qs >= 15:
        print('cok')
        score = calculate_score(right_answer_count)
        session['score'] = score
        return jsonify({'redirect': url_for('end_page')})
    else:
        print('az')
        if round_count < 3:
            id_f = generate_unique_random_f()
            left_text = fake_list[id_f]
            left_image = img_l[id_f]
            round_count += 1

            return jsonify({'image_url':  'static/images/'+left_image ,
                            'first_string':left_text
                            })
        elif round_count >= 3:
            print("burdayinnn")
            id_r = generate_unique_random_r()
            print("buraya r", id_r)
            id_f = generate_unique_random_f()
            print("buraya bak l", id_f)
            right_text = real_list[id_r]
            left_text = fake_list[id_f]
            print(img_l[id_f])
            left_image = img_l[id_f]
            right_image = img_r[id_r]


            print(left_text)
            round_count = 0
            return jsonify({'image_url_r': 'static/images/' + right_image,
                            'right_string': right_text,
                            'image_url': 'static/images/' + left_image,
                            'first_string': left_text
                            })




@app.route('/end')
def end_page():
    score = session.get('score', 79) #79 is placeholder
    score_str = str(score)+'%'
    message = f"{score_str}"
    message_bytes = message.encode('utf-8')
    try:
        #ser.write(b'Hello Arduino!')
        ser.write(message_bytes)
    except:
        print('serial connection failed')
    return render_template('end_page.html',  score=score)

@app.route('/')
def start_page():
     # Data sent must be bytes, not str
    return render_template('welcome.html')

@app.route('/next_right')
def next_file_right():
    global right_text, total_qs, round_count, real_list, left_text, fake_list, img_l, img_r,right_answer_count
    total_qs += 1
    print('right clicked, total_qs:', total_qs)
    print("round count", round_count)
    right_answer_count += 1
    print('correct', right_answer_count)

    if total_qs >= 15:
        score = calculate_score(right_answer_count)
        session['score'] = score
        return jsonify({'redirect': url_for('end_page'),
                        })

    else:
        if round_count<3:
            round_count += 1

            print('we are on the right side')
            id_r = generate_unique_random_r()
            right_text = real_list[id_r]
            img_right = img_r[id_r]
            print("hjhj", right_text)
            #right_image_new_url = list_ims[id_r] #use this later
            return jsonify({'image_url_r': 'static/images/' + img_right,
                            'right_string': right_text
                            })
        elif round_count >=3:
              print("burdayinnn")
              id_r = generate_unique_random_r()
              id_f = generate_unique_random_f()
              right_text = real_list[id_r]
              left_text = fake_list[id_f]
              print(left_text)

              pic_right = img_r[id_r]
              pic_l = img_l[id_f]

              #right_image_new_url = list_ims[id_r]
              #left_image = list_ims[id_r]
              round_count = 0
              return jsonify({'image_url_r': 'static/images/' + pic_right,
                             'right_string': right_text,
                              'image_url': 'static/images/' + pic_l,
                              'first_string': left_text
                              })



@app.route('/get_counter', methods=['GET'])
def get_counter():
    global round_count
    print("adana")
    return jsonify({'counter': round_count})

if __name__ == '__main__':
    socketio.run(app, debug=True)