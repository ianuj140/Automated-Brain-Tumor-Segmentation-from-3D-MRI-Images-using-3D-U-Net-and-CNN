# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 21:07:11 2023

@author: ANUJ
"""
import os
import nibabel as nib
import numpy as np
from tensorflow.keras.models import load_model
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
scaler= MinMaxScaler()
import streamlit as st

model=load_model("D:/pfm/brats2020/brats_3d.hdf5", compile=False)

def preprocess(t1ce_img, t2_img, flair_img):
    flair_img=scaler.fit_transform(flair_img.reshape(-1, flair_img.shape[-1])).reshape(flair_img.shape)
    t1ce_img=scaler.fit_transform(t1ce_img.reshape(-1, t1ce_img.shape[-1])).reshape(t1ce_img.shape)
    t2_img=scaler.fit_transform(t2_img.reshape(-1, t2_img.shape[-1])).reshape(t2_img.shape)

    stacked_img = np.stack([flair_img,t1ce_img, t2_img ], axis=3)

    cropped_img = stacked_img[56:184, 56:184, 13:141, :]

    return cropped_img


def predict_function(img_data):
    img_data_batched = np.expand_dims(img_data, axis=0)
    prediction = model.predict(img_data_batched)
    prediction_argmax = np.argmax(prediction, axis=4)[0, :, :, :]
    return prediction_argmax



def plot_slices(img, mask, prediction, n_slice):
    fig, (ax1,ax2, ax3) = plt.subplots(1, 3, figsize=(12, 8))
    ax1.set_title('Input Image')
    ax1.imshow(img[:, :, n_slice, 1], cmap='gray')
    ax2.set_title('Testing Label')
    ax2.imshow(mask[:, :, n_slice])
    ax3.set_title('Model Prediction')
    ax3.imshow(prediction[:, :, n_slice])
    return fig
