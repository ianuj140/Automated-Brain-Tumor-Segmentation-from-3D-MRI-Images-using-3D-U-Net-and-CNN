# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 00:08:30 2023

@author: ANUJ
"""

import os
import nibabel as nib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
scaler= MinMaxScaler()
import streamlit as st
from utils import preprocess, predict_function, plot_slices



def main():
    st.write(" ")
    st.markdown(
        """
        <div style='background-color:#000000; 
        padding:20px; border: 5px solid #000073;
        box-shadow: 0 0 25px #000073, 0 0 25px #000073, 0 0  25px #000073, 0 0 25px #000073;
        '>
            <p style='font-weight:bold; 
            color:#f5f5f5  ; font-size:33px; font-family:Verdana;'>
            You are currently working on the Brats2021 dataset.
            </p>
            <div style='margin-top:20px;'>
                
        </div>

        """,
        unsafe_allow_html=True
    )
    
    st.write(" ")
    st.write(" ")
    st.write(" ")

    t1ce_file = st.file_uploader("Choose a T1CE NIfTI file", type=["nii", "nii.gz"])
    t2_file = st.file_uploader("Choose a T2 NIfTI file", type=["nii", "nii.gz"])
    flair_file = st.file_uploader("Choose a FLAIR NIfTI file", type=["nii", "nii.gz"])
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.markdown("""
            <style>
            div.stButton > button:first-child {
            background-color: #000000;
            margin: 0 auto;
            font-size: 50px !important;
            font-weight:bold;
            font-family:Verdana;
            
            color: #ffffff;
            display: block;
            width: 340px;
            height: 90px;
            border: 2px solid #000073;
            border-color: #7f00ff;
            box-shadow: 0 0 15px #7f00ff, 0 0 15px #7f00ff, 0 0 15px #7f00ff, 0 0 15px #7f00ff;
            text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.5);
            box-sizing: border-box;


            }

            div.stButton > button:hover {
                background-color: #000000;
                margin: 0 auto;
                font-family:Verdana;
                border-color: #039aff;
                color: #00BFFF;

                text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.5); 
                box-shadow: 0 0 20px #039aff, 0 0 10px #039aff, 0 0 20px #039aff, 0 0 20px #039aff;

                font-weight:bold;
                display: block;
                width: 350px;
                height: 95px;
                border: 3px solid #039aff;
                box-sizing: border-box;
                font-size: 40px;
            }
            """, unsafe_allow_html=True)    

        st.write(" ")
        st.write(" ")
        st.write(" ")

    if st.button("View Segmentation Maps"):
        st.write(" ")
        st.write(" ")
        st.write(" ")
        

        if t1ce_file is not None and t2_file is not None and flair_file is not None:
     
            if not os.path.exists("uploads"):
                os.mkdir("uploads")
    
            t1ce_path = os.path.join("uploads", t1ce_file.name)
            t2_path = os.path.join("uploads", t2_file.name)
            flair_path = os.path.join("uploads", flair_file.name)
            flair_filename = os.path.basename(flair_path)
    
            image_number = flair_filename[10:15]
            parent_directory = r"D:\brats2021\BraTS2021_Training_Data"
            mask_path = os.path.join(parent_directory, f"BraTS2021_{image_number}", f"BraTS2021_{image_number}_seg.nii.gz")
    
            with open(t1ce_path, "wb") as f:
                f.write(t1ce_file.getbuffer())
            with open(t2_path, "wb") as f:
                f.write(t2_file.getbuffer())
            with open(flair_path, "wb") as f:
                f.write(flair_file.getbuffer())
    
            t1ce_img = nib.load(t1ce_path).get_fdata()
            t2_img = nib.load(t2_path).get_fdata()
            flair_img = nib.load(flair_path).get_fdata()
    
            mask_img = nib.load(mask_path)
            mask_img = mask_img.get_fdata()
            mask_img = mask_img.astype(np.uint8)
            mask_img = mask_img[56:184,56:184,13:141]
    
            cropped_img = preprocess(t1ce_img, t2_img, flair_img)
            prediction = predict_function(cropped_img)
            fig = plot_slices(cropped_img, mask_img, prediction, 60)
            st.pyplot(fig)
           
if __name__ == "__main__":
    main()