import cv2
import threading
import mediapipe as mp
import pyautogui
import time
import math
import os
import pygame
import tkinter as tk
import subprocess
import speech_recognition as sr
import keyboard
from gtts import gTTS
import playsound
import requests
import json


def on_button_click():
    root.destroy()


# file voice
def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load('./voice.mp3')
    pygame.mixer.music.play(1)
    root.after(15000, root.destroy)
# day la tui cai phat 2 lan, ong muon may lan thi thay so thoi

# Main code starts here
root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.title("Launch Another Program")

# Set the window size to 1000x667 pixels
root.geometry("1000x667")


# file anh
background_image = tk.PhotoImage(file='./background.gif')

# Create a canvas with the background image
canvas = tk.Canvas(root, width=1000, height=667)
canvas.pack()
canvas.create_image(0, 0, anchor='nw', image=background_image)

# Draw the circular button with white text and blue border
button = tk.Button(root, text='Bắt đầu', font=('Helvetica', 16), fg='white', bg='black', activebackground='gray',
                   activeforeground='white', width=10, height=2, command=on_button_click, bd=5, relief='raised')
button.place(relx=0.69, rely=0.73, relwidth=0.15, relheight=0.1)

# Play the background music when the program starts
play_background_music()

root.mainloop()
print(screen_width,screen_height)


####################################

'''
cap = cv2.VideoCapture(0)
start_time = time.time() 

while True:
    ret, frame = cap.read()
    
    cv2.imshow('frame', frame)
    
    if time.time() - start_time > 10: 
        break
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()

'''


####################################

cap = cv2.VideoCapture(0)

mp_face_mesh = mp.solutions.face_mesh

def track_nose():

  # Lấy kích thước màn hình 
  screen_width, screen_height = pyautogui.size()

  with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5) as face_mesh:

    while True:
      ret, frame = cap.read()
      
      if not ret:
        break

      h = frame.shape[0]
      w = frame.shape[1]

      h_center = h//2
      w_center = w//2

      size_mouse_h = 50
      size_mouse_w = 70

      h_start = h_center - size_mouse_h
      w_start = w_center - size_mouse_w

      h_end = h_center + size_mouse_h
      w_end = w_center + size_mouse_w

      frame = frame[h_start:h_end,w_start:w_end]

      # Phát hiện khuôn mặt
      results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

      ratio_h = round(screen_height/frame.shape[0], 4)
      ratio_w = round(screen_width/frame.shape[1],4)







      if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
          # Lấy tọa độ điểm mũi
          nx, ny = face_landmarks.landmark[1].x, face_landmarks.landmark[1].y
          
          # Chuyển tọa độ tỷ lệ về pixel
          nx = int(nx * frame.shape[1] * ratio_w)
          ny = int(ny * frame.shape[0] * ratio_h)

          pyautogui.moveTo(nx, ny)





def check_left_blink():
  
  with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5) as face_mesh:

    while True:
      ret, frame = cap.read()

      if not ret:
        break

      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    
      results = face_mesh.process(frame)
      
      if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        # Lấy trạng thái nháy mắt phải
        right_eye_top = face_landmarks.landmark[145]
        point_1_right = (right_eye_top.x * frame.shape[1],right_eye_top.y * frame.shape[0])


        right_eye_bottom = face_landmarks.landmark[159]
        point_2_right = (right_eye_bottom.x * frame.shape[1] ,right_eye_bottom.y * frame.shape[0])

        distance_right = math.sqrt((point_2_right[0] - point_1_right[0])**2 + (point_2_right[1] - point_1_right[1])**2)

        #Lấy trạng thái mắt trái
        right_eye_top = face_landmarks.landmark[386]
        point_1_left = (right_eye_top.x * frame.shape[1],right_eye_top.y * frame.shape[0])


        right_eye_bottom = face_landmarks.landmark[374]
        point_2_left = (right_eye_bottom.x * frame.shape[1] ,right_eye_bottom.y * frame.shape[0])

        distance_left = math.sqrt((point_2_left[0] - point_1_left[0])**2 + (point_2_left[1] - point_1_left[1])**2)






        try:
          if distance_right < 4 and distance_left < 4:
            pyautogui.click()
            pygame.mixer.init()
            pygame.mixer.music.load('./click2.mp3')
            pygame.mixer.music.play(1)
          elif distance_left < 4:
            pyautogui.scroll(100)
            print("Nhay mat trai")
          elif distance_right < 4:
            pyautogui.scroll(-100)
            print("Nhay mat phai")



        except Exception:
          pass

      # Đợi một khoảng thời gian
      time.sleep(0.03)

recognizer = sr.Recognizer()
mic = sr.Microphone()

def key_board():

  with mic as source:
    recognizer.adjust_for_ambient_noise(source)
    while True:
      try:
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio, language="vi-VI")
        print(text)

        if text.lower().startswith("hỏi"):
          API_KEY = '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'

          
          prompt = text[3:-1]

          data = {
              'prompt': prompt,
              'temperature': 0.5,
              'max_tokens': 64,
              'top_p': 1,
              'frequency_penalty': 0,
              'presence_penalty': 0
          }

          response = requests.post(
              'https://api.openai.com/v1/engines/text-davinci-003/completions',
              headers={
                  'Content-Type': 'application/json',
                  'Authorization': f'Bearer {API_KEY}'
              },
              json=data
          )
          response_text = json.loads(response.text)['choices'][0]['text']
          print(response_text)
          output = gTTS(response_text,lang="vi", slow=False)
          output.save("output.mp3")
          playsound.playsound('output.mp3', True)

        else:
          keyboard.write(text)

       

        
      except sr.UnknownValueError:
        print("Không hiểu được audio")

# Khởi tạo các luồng
key_board_def = threading.Thread(target=key_board)
nose_thread = threading.Thread(target=track_nose)
blink_thread = threading.Thread(target=check_left_blink)

# Bắt đầu các luồng
key_board_def.start()
nose_thread.start()
blink_thread.start()

# Đợi các luồng kết thúc
key_board_def.join()
nose_thread.join()
blink_thread.join()

# Giải phóng camera
cap.release()