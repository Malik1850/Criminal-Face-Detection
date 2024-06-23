import os
import cv2
import face_recognition
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Tk, Label, Button, filedialog, simpledialog
from datetime import datetime

known_criminals_folder = "images"
screenshot_folder = "screenshots"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

known_encodings = []
known_names = []

def load_known_criminals():
    global known_encodings, known_names
    known_encodings = []
    known_names = []
    for folder_name in os.listdir(known_criminals_folder):
        folder_path = os.path.join(known_criminals_folder, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                image_path = os.path.join(folder_path, file_name)
                if os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    name = folder_name
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        encoding = encodings[0]
                        known_encodings.append(encoding)
                        known_names.append(name)

def get_current_location():
    return 12.9715987, 77.594566

def save_detection_screenshot(frame, name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    latitude, longitude = get_current_location()
    criminal_folder = os.path.join(known_criminals_folder, name)
    if not os.path.exists(criminal_folder):
        os.makedirs(criminal_folder)
    screenshot_path = os.path.join(criminal_folder, f"{name}_{timestamp}.jpg")
    cv2.imwrite(screenshot_path, frame)
    log_path = os.path.join(screenshot_folder, "detection_log.txt")
    with open(log_path, "a") as log_file:
        log_file.write(f"{timestamp}, {name}, Location: (Lat: {latitude}, Lon: {longitude})\n")

def match_criminal():
    match_criminal_from_webcam()

def match_criminal_from_webcam():
    messagebox.showinfo("Match Criminal", "Functionality to match a criminal will be implemented here.")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"
            flag = 1
            if True in matches:
                matched_indices = [index for index, match in enumerate(matches) if match]
                first_match_index = matched_indices[0]
                name = known_names[first_match_index]
                flag = 0
                save_detection_screenshot(frame, name)
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (237, 255, 32), 2)
            if flag == 0:
                cv2.putText(frame, "Matched Criminal: " + name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (158, 49, 255), 2)
            else:
                cv2.putText(frame, "Not Matched", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 37), 2)
            match_label.config(text="Matched Criminal: " + name)
        cv2.imshow('Criminal Identification', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def match_criminal_from_image():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                           filetypes=(("Image Files", ".jpg;.jpeg;.png"), ("All Files", ".*")))
    if file_path:
        image = cv2.imread(file_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"
            flag = 1
            if True in matches:
                matched_indices = [index for index, match in enumerate(matches) if match]
                first_match_index = matched_indices[0]
                name = known_names[first_match_index]
                flag = 0
                save_detection_screenshot(image, name)
            top, right, bottom, left = face_location
            cv2.rectangle(image, (left, top), (right, bottom), (237, 255, 32), 2)
            if flag == 0:
                cv2.putText(image, "Matched Criminal: " + name, (left-40, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (158, 49, 255), 2)
            else:
                cv2.putText(image, "Not Matched", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 37), 2)
            match_label.config(text="Matched Criminal: " + name)
        cv2.imshow('Criminal', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def add_criminal():
    messagebox.showinfo("Add Criminal", "Functionality to add a criminal will be implemented here.")
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                           filetypes=(("Image Files", ".jpg;.jpeg;.png"), ("All Files", ".*")))
    if file_path:
        image = cv2.imread(file_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_image)
        if encodings:
            encoding = encodings[0]
            name = simpledialog.askstring("Add Criminal", "Enter the name of the criminal:")
            if name:
                known_encodings.append(encoding)
                known_names.append(name)
                criminal_folder = os.path.join(known_criminals_folder, name)
                if not os.path.exists(criminal_folder):
                    os.makedirs(criminal_folder)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{timestamp}.jpg"
                save_path = os.path.join(criminal_folder, file_name)
                cv2.imwrite(save_path, image)
                print("Criminal added successfully.")
                load_known_criminals()  # Reload known criminals to refresh encodings and names

def detect_from_image():
    messagebox.showinfo("Detect from Image", "Functionality to detect from an image will be implemented here.")
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                           filetypes=(("Image Files", ".jpg;.jpeg;.png"), ("All Files", ".*")))
    if file_path:
        image = cv2.imread(file_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"
            flag = 1
            if True in matches:
                matched_indices = [index for index, match in enumerate(matches) if match]
                first_match_index = matched_indices[0]
                name = known_names[first_match_index]
                flag = 0
                save_detection_screenshot(image, name)
            top, right, bottom, left = face_location
            cv2.rectangle(image, (left, top), (right, bottom), (237, 255, 32), 2)
            if flag == 0:
                cv2.putText(image, "Matched Criminal: " + name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (158, 49, 255), 2)
            else:
                cv2.putText(image, "Not Matched", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 37), 2)
            match_label.config(text="Matched Criminal: " + name)
        cv2.imshow('Criminal Identification', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

load_known_criminals()

root = tk.Tk()
root.title("Criminal Identification System")
root.geometry("600x400")

# Set the style for the GUI
style = ttk.Style()
style.configure("TLabel", font=("Arial", 14))
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("Header.TLabel", font=("Arial", 18, "bold"))

# Header Label
header_label = ttk.Label(root, text="Criminal Identification System", style="Header.TLabel")
header_label.pack(pady=20)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

match_button = ttk.Button(button_frame, text="Live Detection", command=match_criminal)
match_button.grid(row=0, column=0, padx=10, pady=10)

add_button = ttk.Button(button_frame, text="Add Criminal", command=add_criminal)
add_button.grid(row=0, column=1, padx=10, pady=10)

detect_image_button = ttk.Button(button_frame, text="Detect from Image", command=detect_from_image)
detect_image_button.grid(row=0, column=2, padx=10, pady=10)

# Match Label
match_label = ttk.Label(root, text="Matched Criminal: ")
match_label.pack(pady=20)

# Run the main loop
root.mainloop()