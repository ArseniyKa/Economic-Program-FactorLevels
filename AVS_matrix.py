#!/usr/bin/env python
# coding: utf-8

# In[4]:


# from pip._internal import main as pipmain
# pipmain(['install','openpyxl'])
#use ! before pip
# !pip install scipy
# !pip install matplotlib

from tkinter import *
from tkinter import ttk

from tkinter import font
import pandas as pd
import numpy as np

import Factors as fc
import TableWid as tb
import RisksWid as rk
import GraphWid as gh

import ctypes
###################################################
## Show all columns
pd.set_option("display.max.columns", None)
avs_matrix = np.zeros((4,4))

## default input data
max_score = 1
bin_number = 5
threshold_percent = 0.6
pareto_percent = 0.25
input_list = [max_score, bin_number, threshold_percent, pareto_percent]


# In[5]:


def checking(root):
    try:
            lbl_header=Label(root, text="AVS матрица: ", foreground="#555555", font=("Times New Roman", 35, "bold"), width=22, height=2)
            lbl_header.pack()
            super_frame = Frame(root)
            super_frame.pack()
            #### input widgets
            tb.placeTableWid(input_list, avs_matrix,  "EconomicTable.xlsx", super_frame)

            ##########################################################
            ###############ВТОРАЯ ЧАСТЬ#############################
            #### find nonsistematic coefficient value
            Rsist=10.4
            IRR = 30.99
            risks = fc.Risks(Rsist, IRR)
            risks.calculate(avs_matrix)
            graph = gh.GraphWid(super_frame)
            graph.placeGraph(risks, super_frame) 
            rk.placeRisksWid(risks, super_frame, avs_matrix, graph)
             
    except Exception as e:
             for widget in root.winfo_children():
                widget.destroy()
             print(e)
             root.geometry('900x150+500+500')
             lbl=Label(root, text="Ошибка: пролема с Excel файлом 'EconomicTable.xlsx'\n"+
                "Проверьте есть ли он в текущем каталоге совместно с программой\n"+ 
                "и правильно ли записано имя файла,\n а также названия листов файла", foreground="#333333",
                font=("Times New Roman", 18, "bold"))
             lbl.pack()


# In[6]:


root = Tk()
root.title("Матрица 4x4 AVS")
root.geometry('1360x768+100+60')

# try:
#     img = Image("photo", file="matrix.png", master=root)
#     root.tk.call('wm','iconphoto',root._w, img)   
# except Exception as e:
#     print(e)

checking(root)  
root.mainloop()
                                                            


# In[ ]:




