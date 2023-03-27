#!/usr/bin/env python
# coding: utf-8

# # Optimization of Machine Downtime

# Import the necessary libraries
import streamlit as st
from pycaret.classification import *
import pickle
import os
import sys
import requests
import xgboost
import pandas as pd


# Construct the relative file path to the pickle file
autoML_file = 'autoML_pipeline_lightgbm.pkl'

# Loading the model saved from main.py file
loaded_model = load_model(autoML_file)



st.title('Optimization of Machine Downtime')
st.write('Enter the details below to predict the machine downtime')


# Create a function to predict the machine downtime
def machine_downtime(Hydraulic_Pressure__bar, Coolant_Pressure__bar, Air_System_Pressure__bar,
                     Coolant_Temperature__deg_cel, Hydraulic_Oil_Temperature__deg_cel,
                     Spindle_Bearing_Temperature__deg_cel, Spindle_Vibration__Microm, 
                     Tool_Vibration__Microm, Spindle_Speed__RPM, Voltage__volts, Torque__Nm, Cutting__kN):
    
    input_dict = {'Hydraulic_Pressure__bar': [Hydraulic_Pressure__bar], 
                  'Coolant_Pressure__bar': [Coolant_Pressure__bar], 
                  'Air_System_Pressure__bar': [Air_System_Pressure__bar],
                  'Coolant_Temperature__deg_cel': [Coolant_Temperature__deg_cel], 
                  'Hydraulic_Oil_Temperature__deg_cel': [Hydraulic_Oil_Temperature__deg_cel],
                  'Spindle_Bearing_Temperature__deg_cel': [Spindle_Bearing_Temperature__deg_cel], 
                  'Spindle_Vibration__Microm': [Spindle_Vibration__Microm], 
                  'Tool_Vibration__Microm': [Tool_Vibration__Microm], 
                  'Spindle_Speed__RPM': [Spindle_Speed__RPM], 
                  'Voltage__volts': [Voltage__volts], 
                  'Torque__Nm': [Torque__Nm], 
                  'Cutting__kN': [Cutting__kN]
                  }
    
    input_df = pd.DataFrame.from_dict(input_dict)
    return predict_model(loaded_model, data=input_df)['Label'][0]


# Creating sliders, selectbox, and input_box for taking the input in several ways
Machine_ID = st.selectbox('Machine_ID', ['Makino-L1-Unit1-2013', 'Makino-L3-Unit1-2015', 'Makino-L2-Unit1-2015'])
Assembly_Line_No = st.selectbox('Assembly_Line_No', ['Shopfloor-L1', 'Shopfloor-L3', 'Shopfloor-L2'])
Hydraulic_Pressure__bar = st.number_input('Hydraulic_Pressure__bar', value=101.4, min_value=50.0, max_value=200.0, step=0.1, format='%f')
Coolant_Pressure__bar = st.number_input('Coolant_Pressure__bar', value=4.9, min_value=3.0, max_value=7.0, step=0.1, format='%f')
Air_System_Pressure__bar = st.number_input('Air_System_Pressure__bar', value=6.4, min_value=5.0, max_value=8.0, step=0.1, format='%f')
Coolant_Temperature__deg_cel = st.number_input('Coolant_Temperature__deg_cel', value=18.5, min_value=5.0, max_value=35.0, step=0.1, format='%f')
Hydraulic_Oil_Temperature__deg_cel = st.number_input('Hydraulic_Oil_Temperature__deg_cel', value=47.6, min_value=35.0, max_value=60.0, step=0.1, format='%f')
Spindle_Bearing_Temperature__deg_cel = st.number_input('Spindle_Bearing_Temperature__deg_cel', value=35.06, min_value=20.0, max_value=50.0, step=0.1, format='%f')
Spindle_Vibration__Microm = st.number_input('Spindle_Vibration__Microm', value=1.009, min_value=0.01, max_value=2.00, step=0.01, format='%f')
Tool_Vibration__Microm = st.number_input('TTool_Vibration__Microm', value=25.4, min_value=1.0, max_value=50.0, step=0.1, format='%f')
Spindle_Speed__RPM = st.number_input('Spindle_Speed__RPM', value=20274, min_value=12000, max_value=30000, step=1, format='%d')
Voltage__volts = st.number_input('Voltage__volts', value=349, min_value=200, max_value=480, step=10, format='%d')
Torque__Nm = st.number_input('Torque__Nm', value=25.234, min_value=17.0, max_value=60.0, step=0.1, format='%f')
Cutting__kN = st.number_input('Cutting__kN', value=2.782, min_value=1.0, max_value=5.0, step=0.1, format='%f')


# # Making the prediction
if st.button('Predict Downtime'):
    downtime = machine_downtime(Hydraulic_Pressure__bar, Coolant_Pressure__bar, Air_System_Pressure__bar,
                                Coolant_Temperature__deg_cel, Hydraulic_Oil_Temperature__deg_cel, 
                                Spindle_Bearing_Temperature__deg_cel, Spindle_Vibration__Microm, 
                                Tool_Vibration__Microm, Spindle_Speed__RPM, Voltage__volts, Torque__Nm, Cutting__kN)
    
    if downtime == 1:
        st.success(f'The estimated downtime event is Machine FAILURE')
    else:
        st.success(f'The estimated downtime event is NO Machine failure')
        


