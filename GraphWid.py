#!/usr/bin/env python
# coding: utf-8

import numpy as np
from tkinter import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import font

import Factors as fc

class GraphWid:
      def __init__(self, frame):
            self.color = '#dedede'
            self.figure = Figure(figsize=(5, 3), dpi=85, facecolor=self.color)
            self.plot = self.figure.add_subplot(1, 1, 1)
            self.canvas = FigureCanvasTkAgg(self.figure,frame)
            self.canvas.get_tk_widget().grid(row=0, column=0,padx=(680, 0),  sticky=NW)

      def createGraph(self, risks, plot):
            Rsist =  risks.Rsist
            IRR = risks.IRR
            aggregation_risk_value = risks.aggregation_risk_value
            max_value = max(aggregation_risk_value, IRR)

            x = np.arange(0, 1000, 0.01)
            y = -x + IRR
            f = lambda x: -x + IRR

            xo = aggregation_risk_value
            yo =  f(xo) if f(xo) >= 0 else max_value + 20 - 1
            
            x1 = Rsist
            y1 =  f(x1) if f(x1) >= 0 else max_value + 20 - 1
            
            delta = abs(xo-x1)
            offset = 1 if delta>5 else 7

            plot.plot(x, y)

            plot.set_xlim([0, max_value+20])
            plot.set_ylim([0, max_value+20])
            plot.scatter(xo, yo, color='orange', s=40, marker='o')
            plot.vlines(xo, 0, yo, linestyles ="dashed", colors ="k")
            plot.text(xo-offset, -8,'ra', fontsize=16)

         
            plot.scatter (x1, y1, color='orange', s=40, marker='o')
            plot.vlines(x1, 0, y1, linestyles ="dashed", colors ="k")
            plot.text(x1+offset, -8,'R\u209b', fontsize=16)

            plot.set_xlabel('d,%', loc='right', labelpad=-3)
            plot.set_ylabel('NPV,ден.ед.', labelpad=6 , loc='top')
            plot.set_title("NPV при различных ставках дисконтирования (d)")
            plot.grid()

      


      def placeGraph(self, risks,frame):
            self.plot.clear()
            self.figure.clear()
            self.canvas.get_tk_widget().destroy()            

            self.figure = Figure(figsize=(5, 3), dpi=85, facecolor=self.color)
            self.plot = self.figure.add_subplot(1, 1, 1)
            self.plot.patch.set_facecolor(self.color)
            self.createGraph(risks, self.plot) 

            canvas = FigureCanvasTkAgg(self.figure, frame)
            canvas.get_tk_widget().grid(row=2, column=0, padx=(680, 0), sticky=NW)

    
