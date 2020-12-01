from sklearn.metrics import r2_score
import joblib
import numpy as np

model = int(input('Please choose the model to run \n 1. Cars Price Prediction \n 2. Propulsion Plants Decay Evaluation \n'))
if model != 1 or model != 2:
    print('please enter Number 1 or 2')

if model == 1:
    print('Car price prediction model Loaded')
    car_price_model = joblib.load('car_price_model.pkl')
else:
    print('Propulsion Plants Decay Evaluation Loaded')
    proplusion_model = load_model('propulsion.h5')
        
