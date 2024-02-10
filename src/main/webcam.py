import os
import uuid
import cv2

def capture_image(file_path):
    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)  # 0 indicates the first connected webcam
    
    # Capture a frame
    ret, frame = cap.read()
    
    # Save the captured frame as an image
    cv2.imwrite(file_path, frame)
    
    # Release the webcam
    cap.release()

if __name__ == "__main__":
    relative_path = "../images"
    unique_filename = str(uuid.uuid4()) + ".jpg"
    image_file_path = os.path.join(relative_path, unique_filename)  
    
    # Call the function to capture an image
    capture_image(image_file_path)
    
    print("Image captured and saved at:", image_file_path)
