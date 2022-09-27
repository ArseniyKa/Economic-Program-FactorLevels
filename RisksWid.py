#!/usr/bin/env python
# coding: utf-8

import numpy as np
from tkinter import *

import Factors as fc
import TableWid as tb
import GraphWid as gh
from tkinter import font

lbl_list = [] 
name_Rsist = 'R\u209B'
name_Rnonsist = 'R\u2099\u209B'
in_name_list = ["входные данные", "количество ячеек", "16", name_Rsist+',%', "IRR,%"]
out_name_list = ["выходные данные", "соотношение\nрисков", name_Rnonsist+',%', "агрегированная \nвеличина риска,%"]
    
def placeInputWid(risks, avs_matrix, main_frame, super_frame, graph):
    Rsist =  risks.Rsist
    IRR = risks.IRR
            
    frame1 = Frame(main_frame)
    frame1.grid(row=0, column=0, sticky=NSEW, padx=60, pady=(20,20))
             
    str_Rsist = StringVar(main_frame)
    str_IRR = StringVar(main_frame)
    
    str_Rsist.set(float(Rsist))
    str_IRR.set(float(IRR))    
    str_var_list = [str_Rsist, str_IRR]
    
    for i, j in zip( range(len(in_name_list)), (0,1,2,3,5)):
        color = '#dddddd' if i !=0 else '#c0c0c0'
        lbl_name = Label(frame1, text = in_name_list[i], background = color, font='Times 14', relief=RIDGE)
        lbl_name.grid(row=j, column=0, sticky=NSEW)            
             
    for i, j in zip( (4, 6), (0,1) ):
        spin_box = Spinbox(frame1, from_=0, to= 100, increment=1,justify = CENTER, font='Times 14', 
         bg='#eeeeee', textvariable = str_var_list[j], wrap=True)
        spin_box.grid(row=i, column=0, sticky=NSEW) 
                         
    button = Button(frame1, text="Рассчитать", width=20, command=lambda: changeOutputSlot(risks, lbl_list,
    avs_matrix, str_var_list, super_frame, graph))
    button.grid(row = 7, column=0, sticky=NSEW)
    
########################OUTPUT WIDGET
def placeOutputWid(risks, main_frame):
    Rnonsist = risks.Rnonsist            
    k = risks.k
    aggregation_risk_value = risks.aggregation_risk_value
    result_list = [str(k), str(Rnonsist), str(aggregation_risk_value)]
    
    frame2 = Frame(main_frame)
    frame2.grid(row=0, column=1, sticky=NSEW, padx=60, pady=(20,20))
         
    for i, j in zip( range(len(out_name_list)), (0,1,3,5)):
        color = '#dddddd' if i !=0 else '#c0c0c0'
        label = Label(frame2, text = out_name_list[i], background=color, font='Times 13', relief=RIDGE)
        label.grid(row=j, column=0, sticky=NSEW)
        
    for i, j in zip( range(len(result_list)), (2,4,6)):
        label = Label(frame2, text = result_list[i], font='Times 13', relief=RIDGE)
        label.grid(row=j, column=0, sticky=NSEW)
        lbl_list.append(label)
 


def placeRisksWid(risks, super_frame, avs_matrix, graph):

    main_frame = Frame(super_frame, highlightbackground = "#606060",  highlightthickness=2)
    main_frame.grid(row=2, column=0, padx=(20,30), pady=(20,0), sticky= NW)
    
    placeInputWid(risks, avs_matrix, main_frame, super_frame, graph)
    placeOutputWid(risks, main_frame)

        
        
def changeOutputSlot(risks, lbl_list, avs_matrix, str_var_list, super_frame, graph):
    risks.Rsist=int(str_var_list[0].get())
    risks.IRR=int(str_var_list[1].get())
    risks.calculate(avs_matrix)
    Rsist= risks.Rsist
    Rnonsist = risks.Rnonsist
    k = risks.k
    aggregation_risk_value = risks.aggregation_risk_value
    IRR = risks.IRR
    output_list = [str(k), str(Rnonsist), str(aggregation_risk_value)]
    
    for i in range(len(output_list)):
        lbl_list[i]['text'] = output_list[i]
        
    graph.placeGraph(risks, super_frame)
    