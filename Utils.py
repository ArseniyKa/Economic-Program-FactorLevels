#!/usr/bin/env python
# coding: utf-8

# from pip._internal import main as pipmain
# pipmain(['install','openpyxl'])
# use ! before pip
# !pip install scipy

import pandas as pd
import numpy as np

import Factors as fc

cell_name_list = ["Н/Э", "Н/А", "Н/Т", "Н/С", "Р/Э", "Р/А", "Р/Т", "Р/С",
                  "О/Э", "О/А", "О/Т", "О/С", "П/Э", "П/А", "П/Т", "П/С"]


def calculate(input_list, result_list, avs_matrix, sheet_name):
    for i in range(16):       
        list_name = cell_name_list[i].replace('/', '_')    
        df = pd.read_excel(sheet_name, sheet_name=list_name)
        fact = fc.Factors(df, input_list)
        fact.calculate()
        value = fact.table_value        
        dominant_factors =fact.dominant_factors_name_list       
        result_list[i] = (value, dominant_factors)
        initializeMatrixValue(value, i, avs_matrix)  
        
def initializeMatrixValue(value, index, avs_matrix):    
    (x, y) = getColumnRow(index, 4)
    avs_matrix[y][x] = value

    
def getColumnRow(index, size):
    column = int(index)%size
    row = int(index)//size
    return (column,row)    





