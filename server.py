from flask import Flask, render_template, jsonify, session, url_for
from flask_socketio import SocketIO
import pandas as pd
import random
import serial
import content_class


try:
    ser = serial.Serial('/dev/cu.usbmodemHIDPC1', 9600, timeout=1)
except:
    print("PORT NOT FOUND")
import random
previous_numbers_f = set()
previous_numbers_r = set()
def generate_unique_random_f():
    global previous_numbers
    while True:
        num = random.randint(0, 15)
        if num not in previous_numbers_f:
            previous_numbers_f.add(num)
            return num

def generate_unique_random_r():
    global previous_numbers_r
    while True:
        num = random.randint(0, 14)
        if num not in previous_numbers_r:
            previous_numbers_r.add(num)
            return num

round_count = 0
total_qs = 0

img_l = []
img_r = []

for i in range(16):
    if i!=0:
        img_l.append("f"+str(i)+".jpg")
        img_r.append("r" + str(i) + ".jpg")
print(img_r)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

list_ims = ["image1.png","image2.png","image3.png"]
text_long = "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsu"
#list_headlines = ["adana", text_long,"istanbul", "brooklyn"]



fake_list = [
 "Exclusive: Erdogan Caught Photoshopping Extra Crowds into His Rally Pictures for 'More Impact’",

  "Turkey's Education System Under Scrutiny: Critics Accuse Erdogan's Government of Ideological Agenda",

  "Drunk man accidentally takes $1,600 Uber from West Virginia to New Jersey",

  "SNL star, Donald Trump Jr-Aubrey O'Day cheating scandal resurface",

  "Man contracts rare infection likely during cockroach-related activities, confirmed in China",

  "Levin: Biden has unleashed a housing apocalypse on America as Americans scramble to move out of cities",

  "NYC's $2,000 Fine for Posting a 'Hate Speech' Sign set off a  Supreme Court debate on anti-bias laws",

  "Up to 36 million vote-by-mail ballots could go missing in 2020, a new study says",

  "Madonna predicted the COVID-19 outbreak in creepy bath video: 'It's the great equalizer’",

  "Sweden bans balloons from Royal Wedding 'due to the environmental impact'",

  "NYC voters waking up to find presidential ballot error that could cost Biden votes on local races",

  "Biden suffers another major legal defeat in fight over weakened ICE deportations",

"GameStop Claims It’s an “Essential Business” to Stay Open During Coronavirus Closures",

"Cyberpunk 2077 delayed, doing 'more crunch than maybe have been necessary'",
"Astronomers are worried about more and more satellites forming 'megaconstellations' around Earth after SpaceX launched nearly 50 Friday"
]

real_list = [
"Erdogan risks losing power as Turkey's high-stakes election reaches its climax",

"Erdogan's rival boosted by withdrawal, poll lead ahead of Turkey vote",

"US Military Could Lose Space Force Trademark to Netflix Series",

"White House threatens to fire anyone who tries to quit",

"United States Risks Sanctions From Zimbabwe If Elections Are Not Free And Fair",

"Trump was 'not wrong' when he warned criminals are coming across US border: Tom Homan",

"Trump promotes 'God Bless the USA' Bible",

"Rapper 50 Cent admits he thinks Trump's 'gonna be president again",

"Hillary Clinton warns AI tech will make 2016 election disinformation 'look primitive'",

"Microsoft says a Russian hacking group is still trying to crack into its systems",
"Reddit CEO tells user, “we are not the thought police,” then suspends that user",
  "Ben Affleck finally achieves lifelong dream of not having to play Batman anymore",
  "McDonald's robber demands chicken nuggets, has to accept breakfast food because it was still too early",
  "North Korean Founder Kim Il Sung Did Not Have the Ability to Teleport, State Media Admits",
    "Tim Cook says employees who leak memos do not belong at Apple, according to leaked memo"
]



current_index = 0
right_im_index = 0
first_image_url = list_ims[current_index]
#first_text = list_headlines[current_index]
#right_text = list_headlines[right_im_index]

first_text = fake_list[0]
right_text = real_list[0]

def calculate_score():
    value = random.randint(60, 90)
    return value


@app.route('/index')
def index():
    global total_qs, current_index,right_im_index, round_count, previous_numbers_f,previous_numbers_r
    total_qs = 0
    current_index = 0
    right_im_index = 0
    round_count = 0
    previous_numbers_f = set()
    previous_numbers_r = set()

    print("hello worl index page loaded, variables set to 0")
    df = pd.read_csv('images.csv')  # Assuming your CSV file is named 'data.csv'
    #first_image_url = df.iloc[0,0] # Assuming 'image_url' is the column containing image URLs
    first_image_url = img_l[0]
    first_right_image = img_r[0]
    #return render_template('index.html', first_image_url=first_image_url)

    first_text = fake_list[0]
    right_text = real_list[0]
    #print('heyaaa', first_text)



    return render_template('index.html', first_image_url=first_image_url,  first_string=first_text, right_image_url=first_right_image, right_string=right_text)

# @socketio.on('connect')
# def handle_connect():
#     df = pd.read_csv('images.csv')  # Assuming your CSV file is named 'data.csv'
#     data = df.to_dict(orient='records')
#     print(data)
#     socketio.emit('csv_data', data)
# #newww
#     image_urls = df.iloc[:, 0].tolist()  # Assuming URLs are in the first column
#
#     # Send CSV data (image URLs) to the client
#     socketio.emit('csv_data', image_urls)

@app.route('/next')
def next_file():
    global current_index, first_image_url, first_text, list_headlines,total_qs,round_count,img_l,im_r
    current_index = (current_index + 1) % len(list_ims)
    total_qs += 1
    print('left clicked, total_qs:', total_qs)
    if total_qs >= 15:
        print('cok')
        score = calculate_score()
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
            print("liste: ", img_l)
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
    global right_im_index, right_text, total_qs, round_count, real_list, left_text, fake_list, img_l, img_r
    total_qs += 1
    print('right clicked, total_qs:', total_qs)
    print("round count", round_count)
    if total_qs >= 15:
        score = calculate_score()
        session['score'] = score
        return jsonify({'redirect': url_for('end_page'),
                        })

    else:
        if round_count<3:
            round_count += 1

            # right_im_index = (right_im_index + 1) % len(list_ims)
            print('we are on the right side', right_im_index)
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