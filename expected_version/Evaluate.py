# -*- coding: utf-8 -*-
"""
Created on Sun May 25 14:44:28 2025

@author: maxtr
"""

def mean_absolute_error(user_id):
    prediction = np.array(predict_rate(user_id))
    mae = np.abs(Rating.ratings - prediction).mean()

def root_mean_square_error():
    prediction = np.array(predict_rate(user_id))
    rmse = np.sqrt(((Rating.ratings - prediction)**2).mean())