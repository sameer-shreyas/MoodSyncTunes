from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from tensorflow.keras.models import load_model
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Route to render the HTML template
@app.route('/')
def home():
    return render_template('index.html')

# Load the facial emotion recognition model
emotion_model = load_model('CNN_Final_Modelv2.h5')

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Emotion labels
emotions = ['#Angry', '#Disgust', '#Fear', '#Happy', '#Neutral', '#Sad', '#Surprised']

# Function to perform facial emotion recognition
def predict_emotion(image_data):
    try:
        # Convert base64 image to PIL Image
        image = Image.open(BytesIO(base64.b64decode(image_data.split(',')[1])))

        # Convert PIL Image to OpenCV format
        frame1 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        frame1 = cv2.resize(frame1, (600, 500))
        
        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        # Detect faces
        num_faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        predicted_labels = []

        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame1, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = cv2.resize(roi_gray_frame, (48, 48))
            cropped_img = cropped_img.astype("float") / 255.0
            cropped_img = np.expand_dims(cropped_img, axis=0)

            # Predict emotion
            prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            predicted_labels.append(emotions[maxindex])

        return predicted_labels[0] if predicted_labels else None
    except Exception as e:
        print(f"Error in predict_emotion: {e}")
        return None

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data.get('image')

    # Perform facial emotion recognition
    predicted_label = predict_emotion(image_data)

    # Return result as JSON
    return jsonify({'predicted_label': predicted_label})

if __name__ == '__main__':
    app.run(debug=True)