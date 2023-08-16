import streamlit as st
import cv2
import numpy as np
from paddleocr import PaddleOCR
from utils import process_ocr_results

ocr = PaddleOCR(use_angle_cls=True,
    ocr_version="PP-OCRv4") 

# Function to process images and return results
def process_images(left_image, right_image):
    # Process left image and get results
    left_results = ocr.ocr(left_image)
    left_processed_image, left_processed_texts= process_ocr_results(left_image,left_results)  # Replace with your processing logic
    
    # Process right image and get results
    right_results = ocr.ocr(right_image)
    right_processed_image, right_processed_texts= process_ocr_results(right_image,right_results )# Replace with your processing logic
    
    return left_processed_image, left_processed_texts, right_processed_image, right_processed_texts

# Streamlit UI
st.title("OCR Demo")


# Upload images
left_image = st.file_uploader("Upload Left Workstation Image", type=["jpg", "png"])
right_image = st.file_uploader("Upload Right Workstation Image", type=["jpg", "png"])

# Submit button
if st.button("Submit"):
    if left_image and right_image:
        left_image = cv2.imdecode(np.fromstring(left_image.read(), np.uint8), 1)
        right_image = cv2.imdecode(np.fromstring(right_image.read(), np.uint8), 1)
        
        left_processed, left_results, right_processed, right_results = process_images(left_image, right_image)
        

        col1, col2 = st.columns(2)
        
        with col1:
            st.image(left_processed, caption="Processed Left Workstation Image", use_column_width=True)
            st.write(f"Dot-Peening Text: {left_results[0]}")
            st.write(f"Machine-Peening Text: {left_results[1]}")
            
        with col2:
            st.image(right_processed, caption="Processed Right Workstation Image", use_column_width=True)
            st.write(f"Dot-Peening Text: {right_results[0]}")
            st.write(f"Machine-Peening Text: {right_results[1]}")
       
        if( (left_results[0] == right_results[0]) and left_results[1] == right_results[1]):
            st.write('Match Status: OK')
        else:
            st.write('Match Status: NOT OK')
# Refresh button
if st.button("Refresh"):
    # Clear uploaded images
    left_image = None
    right_image = None
    # Clear previous results
    st.session_state.pop('left_results', None)
    st.session_state.pop('right_results', None)
    st.session_state.left_image = None
    st.session_state.right_image = None
    