from flask import Flask, render_template, jsonify, session
from flask_socketio import SocketIO
import pandas as pd
import content_class

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

list_ims = ["image1.png","image2.png","image3.png"]
text_long = "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsu"
list_headlines = ["adana", text_long,"istanbul", "brooklyn"]
current_index = 0
right_im_index = 0
first_image_url = list_ims[current_index]
first_text = list_headlines[current_index]

@app.route('/')
def index():
    df = pd.read_csv('images.csv')  # Assuming your CSV file is named 'data.csv'
    #first_image_url = df.iloc[0,0] # Assuming 'image_url' is the column containing image URLs
    first_image_url = list_ims[current_index]
    first_right_image = list_ims[right_im_index]
    #return render_template('index.html', first_image_url=first_image_url)

    first_text = list_headlines[current_index]
    #print('heyaaa', first_text)



    return render_template('index.html', first_image_url=first_image_url,  first_string=first_text, right_image_url=first_right_image)

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
    global current_index, first_image_url, first_text, list_headlines
    current_index = (current_index + 1) % len(list_ims)
    print(current_index)
    first_image_url = list_ims[current_index]
    first_text = list_headlines[current_index]
    print(first_text)



    return jsonify({'image_url':  'static/images/'+first_image_url,
                    'first_string':first_text
                    })


@app.route('/next_right')
def next_file_right():
    global right_im_index
    right_im_index = (right_im_index + 1) % len(list_ims)
    print('we are on the right side', right_im_index)

    right_image_new_url = list_ims[right_im_index]
    return jsonify({'image_url': 'static/images/' + right_image_new_url})

if __name__ == '__main__':
    socketio.run(app, debug=True)