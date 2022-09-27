#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from tkinter import *
import tkinter.ttk as ttk
import Factors as fc
import Utils as uti
from tkinter import font


# it will be global variables
row_header_list = ["Экономические", "Административно-правовые", "Ресурсно-технические", "Социально-экологические"]
column_header_list = ["Национальная экономика (Н)", "Регион (Р)", "Отрасль (О)", "Предприятие (П)"]
in_header_list = ["максимальный \nоценочный бал", "число \nразбиений", "порог \nсогласованности,%",
                  "число Паретто,%"]


################################  
def placeInputWidgets(input_list, result_list, avs_matrix, sheet_name, super_frame):
    frame = Frame(super_frame, highlightbackground = "#606060",  highlightthickness=2)
    frame.grid(row=0,column=0, padx=(30,0), sticky='w')
    vars = []
    padding = (0, 5)
    
    
    for i in range(len(input_list)):
        var = StringVar(super_frame)
        lbl = Label(frame, font='Times 14', text = in_header_list[i])
        lbl.grid(row=0, column=i, pady=padding, sticky=NSEW)
        
        max_value =10000 if i<2  else 1
        step = 1 if i<2 else 0.1
        spin_box = Spinbox(frame, from_=0, to= max_value, increment=step, font='Times 14',
         bg='#eeeeee',   justify = CENTER, textvariable=var,  wrap=True)
        spin_box.grid(row=1, column=i, pady=padding, sticky=NSEW)
        var.set(input_list[i])
            
        vars.append(var)
    btn = Button(frame, text="Рассчитать", command=lambda:[initializeInputList(input_list, vars),
                                uti.calculate(input_list, result_list, avs_matrix, sheet_name)])
    btn.grid(row=1, column=len(input_list), padx=40, pady=padding, sticky= NSEW)  


def createTableHeaders(frame): 
    color = '#c0c0c0'
    corner_cell = Label(frame, background=color, relief=RIDGE).grid(row=0, column=0, sticky=NSEW)
    for x in range(4):
        row_header=Label(frame, text= row_header_list[x], font='Times 16',background= color,  relief=RIDGE)
        row_header.grid(row=0, column=x+1,sticky=NSEW)
        
        column_header = Label(frame, text= column_header_list[x], font='Times 16', background= color, relief=RIDGE)
        column_header.grid(row=x+1, column=0, sticky=NSEW) 

def initializeInputList(input_list, vars):        
    for i in range(len(vars)):
        default_value = int(vars[i].get()) if i<2 else float(vars[i].get())
        input_list[i] = input_list[i] if vars[i].get() =='' else default_value
    

def placeTableWid(input_list, avs_matrix, sheet_name, super_frame):
    ### additional variables
    matrix_size = 16
    result_list = [None] * matrix_size
    btn_list = [None] * matrix_size
    
    placeInputWidgets(input_list,result_list, avs_matrix, sheet_name, super_frame) 

    frame = Frame(super_frame)
    frame.grid(row=1, column=0, pady=(20,0), padx=(30,0))
    createTableHeaders(frame)     
    uti.calculate(input_list, result_list, avs_matrix, sheet_name)
    createBtnList(btn_list, result_list, super_frame, frame)

    button = Button(frame, text="Показать значения", width=20, command=lambda: changeBtnTextSlot(btn_list, avs_matrix))
    button.grid(row=5, column=0, pady=(20,0),  sticky='w')
################################  

def showResultSlot(data_list, super_frame):
    value = data_list[0]
    dominant_factors =data_list[1]

    win = Toplevel(super_frame)
    win.title("Результаты")
    win.geometry('950x400+200+200')   
    
    frame = Frame(win)
    frame.place(x=50, y=30)

    lbl_value = Label(frame, text="Значение в ячейке = " + str(round(value,3)), font='Times 24',  relief=RIDGE,  anchor='w')
    lbl_value.grid(row=0, column=0, sticky='w', pady = (0,30))
           
    lbl_header = Label(frame, text="Доминирующие факторы: ",background='#c0c0c0', font='Times 24',relief=RIDGE)
    lbl_header.grid(row=1, column=0,sticky=NSEW)
    
    for i in range(len(dominant_factors)):
        lbl_factors=Label(frame, text=str(dominant_factors[i]), wraplength=800, font='Times 22',relief=RIDGE, anchor='w')
        lbl_factors.grid(row= i + 2, column=0,sticky=NSEW)
     
    frame.update()
    width = frame.winfo_width()
    height = frame.winfo_height()
    win.geometry('%dx%d+300+300' % (width+100, height+80) )

    win.mainloop()
    
    
    
    
################################ 

def changeBtnTextSlot(btn_list, avs_matrix):
      print("avs matrix\n", avs_matrix)
      if btn_list[0]["state"] == "normal":
          resized_arr = avs_matrix.flatten()
          for i in range(len(btn_list)):
            btn_list[i]['text'] = round(resized_arr[i],3)
            btn_list[i]["state"] = "disabled"
      else:
          for i in range(len(btn_list)):
            btn_list[i]['text'] = uti.cell_name_list[i]
            btn_list[i]["state"] = "normal"
                        

def createBtnList(btn_list, result_list, super_frame, frame):    
    for i in range(16):
        (x, y) = uti.getColumnRow(i, 4)
###Без лямбды будет сразу срабатывать 
        btn = Button( frame, text = uti.cell_name_list[i], width=17,
              disabledforeground="black",
              command=lambda i=i: showResultSlot(result_list[i], super_frame) ) 
        btn['font'] = font.Font(family='Helvetica', size=14)                
        btn.grid(row=y+1, column=x+1,sticky=NSEW)
        btn_list[i] = btn

    return btn_list                