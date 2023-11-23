# MoodSyncTunes

MoodSyncTunes is a project that uses facial emotion recognition to detect the user's mood through their webcam and recommends songs based on the predicted emotion. The application is built using Flask for the backend and HTML/CSS, JavaScript for the frontend. It leverages a pre-trained Convolutional Neural Network (CNN) model for facial emotion recognition.

## Features

- **Facial Emotion Recognition:** The application uses a pre-trained CNN model to analyze facial expressions and predict the user's emotion in real-time.

- **Webcam Integration:** Users can open their webcam, and the application captures snapshots to analyze facial expressions.

- **Song Recommendations:** Based on the predicted emotion, the application recommends songs that match the user's mood.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python (3.x recommended)
- Flask
- OpenCV
- TensorFlow
- PIL (Python Imaging Library)
- NumPy

Install the required Python packages using:

```bash
pip install flask opencv-python tensorflow pillow numpy
```

## Getting Started

1.  Clone the repository:

```bash
git clone https://github.com/your-username/MoodSyncTunes.git
cd MoodSyncTunes
```

2  .Run the Flask application:

```bash
python main.py
```

3.   Open a web browser and go to http://localhost:5000.

4.  Click on the "Open Webcam" button to activate your webcam.

5.  Capture snapshots to analyze facial expressions and receive song recommendations.

## Folder Structure

**static/**: Contains static files such as images and CSS.

**emojis/**: Emoji images corresponding to different emotions.

**templates/**: HTML templates for the frontend.

**index.html**: Main page template.

**main.py**: Flask application script.

**CNN_Final_Modelv2.h5**: Pre-trained CNN model for facial emotion recognition.

**haarcascade_frontalface_default.xml**: Haar Cascade for face detection.

**FER.py**: Flask application script for real time facial emotion recognition

**FERmodel.ipynb**: kaggle notebook for training the model

