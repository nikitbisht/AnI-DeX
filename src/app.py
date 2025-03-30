from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io
import requests

model = load_model('model/inception.h5')

class_dic = {
    0: 'antelope',
    1: 'badger',
    2: 'bat',
    3: 'bear',
    4: 'bee',
    5: 'beetle',
    6: 'bison',
    7: 'boar',
    8: 'butterfly',
    9: 'cat',
    10: 'caterpillar',
    11: 'chimpanzee',
    12: 'cockroach',
    13: 'cow',
    14: 'coyote',
    15: 'crab',
    16: 'crow',
    17: 'deer',
    18: 'dog',
    19: 'dolphin',
    20: 'donkey',
    21: 'dragonfly',
    22: 'duck',
    23: 'eagle',
    24: 'elephant',
    25: 'flamingo',
    26: 'fly',
    27: 'fox',
    28: 'goat',
    29: 'goldfish',
    30: 'goose',
    31: 'gorilla',
    32: 'grasshopper',
    33: 'hamster',
    34: 'hare',
    35: 'hedgehog',
    36: 'hippopotamus',
    37: 'hornbill',
    38: 'horse',
    39: 'hummingbird',
    40: 'hyena',
    41: 'jellyfish',
    42: 'kangaroo',
    43: 'koala',
    44: 'ladybugs',
    45: 'leopard',
    46: 'lion',
    47: 'lizard',
    48: 'lobster',
    49: 'mosquito',
    50: 'moth',
    51: 'mouse',
    52: 'octopus',
    53: 'okapi',
    54: 'orangutan',
    55: 'otter',
    56: 'owl',
    57: 'ox',
    58: 'oyster',
    59: 'panda',
    60: 'parrot',
    61: 'pelecaniformes',
    62: 'penguin',
    63: 'pig',
    64: 'pigeon',
    65: 'porcupine',
    66: 'possum',
    67: 'raccoon',
    68: 'rat',
    69: 'reindeer',
    70: 'rhinoceros',
    71: 'sandpiper',
    72: 'seahorse',
    73: 'seal',
    74: 'shark',
    75: 'sheep',
    76: 'snake',
    77: 'sparrow',
    78: 'squid',
    79: 'squirrel',
    80: 'starfish',
    81: 'swan',
    82: 'tiger',
    83: 'turkey',
    84: 'turtle',
    85: 'whale',
    86: 'wolf',
    87: 'wombat',
    88: 'woodpecker',
    89: 'zebra'
}


def preprocessing(img):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((224,224))
    img_array = np.array(img).astype('float32')
    img_array /=255.0
    img_array = np.expand_dims(img_array,axis=0)
    return img_array



app = Flask(__name__)
@app.route('/')
def frontEnd():
    return render_template("index.html")


@app.route('/predict',methods=['POST'])
def predict():
    image_file = request.files['image']
    print(image_file.filename)
    if image_file.filename.lower().endswith('.heic'):
        return jsonify({
            'prediction':'HEIC format not supported. please upload JPG or PNG.'
        })
    img = image.load_img(io.BytesIO(image_file.read()), target_size=(224, 224))
    img_array = preprocessing(img)
    predictions = model.predict(img_array)
    prediction_indices = np.argmax(predictions)
    output = class_dic[prediction_indices]
    # print(output)
    return jsonify({
        'prediction':output
    })



@app.route('/fetch_animal_details/<animal_name>', methods=['GET'])
def fetch_animal_details(animal_name):
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={animal_name}&prop=extracts|images&exintro=true&explaintext=true&format=json"
    response = requests.get(url)
    data = response.json()
    pages = data.get('query',{}).get('pages',{})
    page = next(iter(pages.values()),{})

    extract_text = page.get("extract","Sorry No infromation available")
    sentances = extract_text.split(". ")[:5]
    extract_text = '. '.join(sentances) 
    if len(extract_text) < 10:
        extract_text = "Sorry No infromation available"
    images = page.get('images',[])
    valid_extensions = (".jpg", ".jpeg", ".png", ".svg", ".gif")
    
    image_titles = []
    cnt = 0
    for img in images:
        if(img['title'].lower().endswith(valid_extensions)):
            image_titles.append(img['title'])
            cnt +=1
        if cnt >= 3:
            break

    return jsonify({
        'extract':extract_text,
        'images': image_titles
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
