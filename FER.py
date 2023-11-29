import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import threading

emotion_model = load_model('model/CNN_Final_Modelv2.h5')
cv2.ocl.setUseOpenCL(False)

emotion_dict = {0: "   Angry   ", 1: "Disgusted", 2: "  Fearful  ", 3: "   Happy   ", 4: "  Neutral  ", 5: "    Sad    ", 6: "Surprised"}

emoji_dist = {
    0: "static/emojis/Angry.png",
    1: "static/emojis/Disgusted.png",
    2: "static/emojis/Fear.png",
    3: "static/emojis/happy.png",
    4: "static/emojis/Neutral.png",
    5: "static/emojis/Sad.png",
    6: "static/emojis/Surprised.png"
}

global last_frame1
last_frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
show_text = [0]
global frame_number
capture_active = True  # Flag to toggle camera feed

def show_subject():
    global frame_number
    cap1 = cv2.VideoCapture(0)
    
    if not cap1.isOpened():
        print("Error: Webcam not open")
        return

    while True:
        if capture_active:
            _, frame1 = cap1.read()
            frame1 = cv2.resize(frame1, (600, 500))
            gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            bounding_box = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            num_faces = bounding_box.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in num_faces:
                cv2.rectangle(frame1, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                roi_gray_frame = gray_frame[y:y + h, x:x + w]
                cropped_img = cv2.resize(roi_gray_frame, (48, 48))
                cropped_img = cropped_img.astype("float") / 255.0
                cropped_img = img_to_array(cropped_img)
                cropped_img = np.expand_dims(cropped_img, axis=0)
                
                prediction = emotion_model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                
                cv2.putText(frame1, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                show_text[0] = maxindex

            global last_frame1
            last_frame1 = frame1.copy()
            pic = cv2.cvtColor(last_frame1, cv2.COLOR_BGR2RGB)     
            img = Image.fromarray(pic)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            root.update()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap1.release()
    cv2.destroyAllWindows()  # Release OpenCV resources

def show_avatar():
    while True:
        if capture_active:
            frame2 = cv2.imread(emoji_dist[show_text[0]])
            pic2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            img2 = Image.fromarray(frame2)
            imgtk2 = ImageTk.PhotoImage(image=img2)
            lmain2.imgtk2 = imgtk2
            lmain3.configure(text=emotion_dict[show_text[0]], font=('arial', 45, 'bold'))
            
            lmain2.configure(image=imgtk2)
            root.update()

def toggle_capture():
    global capture_active
    capture_active = not capture_active

def on_quit():
    root.destroy()


if __name__ == '__main__':
    frame_number = 0
    root = tk.Tk()

    root.image = ImageTk.PhotoImage(Image.open("logo.png"))
    header_label = tk.Label(root, image=root.image, bg='black')
    header_label.pack(pady=10)

    lmain = tk.Label(master=root, padx=30, bd=10)
    lmain2 = tk.Label(master=root, bd=10)
    lmain3 = tk.Label(master=root,padx=30, bd=10, fg="#CDCDCD", bg='black')
    lmain.pack(side=LEFT)
    lmain.place(x=40, y=250)
    lmain3.pack()
    lmain3.place(x=960, y=250)
    lmain2.pack(side=RIGHT)
    lmain2.place(x=900, y=350)

    pause_button = Button(root, text='Pause/Resume',fg="black", command=toggle_capture, font=('arial', 15, 'bold'))
    pause_button.pack(side=TOP)

    root.title("Emotion_Recognition_Model")
    root.geometry("1400x900+100+10")
    root['bg'] = 'red'
    exitbutton = Button(root, text='Quit', fg="black", command=on_quit, font=('arial', 25, 'bold'))
    exitbutton.pack(side=BOTTOM)
    
    threading.Thread(target=show_subject).start()
    threading.Thread(target=show_avatar).start()
    
    root.mainloop()
