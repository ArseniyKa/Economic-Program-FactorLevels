#!/usr/bin/env python
# coding: utf-8

import numpy as np

coeff_pairs  = [(0, 0), (1, 0.053), (2, 0.111), (3, 0.176), (4, 0.25), (5, 0.333),
               (6, 0.428), (7, 0.538), (8, 0.666), (9, 0.818),
               (10, 1), (11,1.222), (12, 1.5), (13, 1.857), (14, 2.333), (15,3), (16, 4) ]

## первая часть для расчета гистограмм
class Factors:
    def __init__(self, df, data_list):
        self.df= df
        self.max_score = data_list[0]
        self.bin_number = data_list[1]
        self.threshold_percent = data_list[2]
        self.pareto_percent = data_list[3]
    
    
    def calculate(self):        
        ## input data       
        max_score = self.max_score
        bin_number = self.bin_number
## number of bins is bin_number, size of the array is bin number +1 
        bins = np.linspace(0, max_score, bin_number+1)
            
        df =self.df
        ###### arr[i][j] first index is rows(y) and the second one is columns(x)
        arr = self.df.to_numpy()
        columns_names = df.columns.values
        data_matrix= arr[:,1:]
        xsize = data_matrix[0].size
        ysize = data_matrix[:,0].size
        
        threshold_percent = self.threshold_percent
        threshold = threshold_percent * ysize
        
        non_zero_factor_list = []
        dominant_factors_name_list = []
        
## create a histogram for each column
        for i in range(xsize):
            factor_mean_value = self.createHistogram(data_matrix, columns_names, bins, threshold, i)
            if factor_mean_value != 0:
                non_zero_factor_list.append(factor_mean_value)
                dominant_factors_name_list.append(columns_names[i+1])

        self.addParettoCondition(non_zero_factor_list, dominant_factors_name_list, xsize)  
        
        
    def createHistogram(self, data_matrix, columns_names, bins, threshold, i):            
            column = data_matrix[:, i]
            hist, bins = np.histogram(column, bins = bins)

            max_hist_value = np.max(hist)            
            if max_hist_value>=threshold:
                hist_index = np.argmax(hist)
                left_bin_edge = bins[hist_index]         
                rigth_bin_edge = bins[hist_index + 1]
                
                #### choose good elements from the column in the whole bin
                elements_in_bin = column[ (column >=left_bin_edge) * (column <= rigth_bin_edge) ]
                return np.mean(elements_in_bin)
            else:
                return 0
 
        

    def addParettoCondition(self, non_zero_factor_list, dominant_factors_name_list, xsize):
            pareto_percent = self.pareto_percent
            pareto_value = int(xsize * pareto_percent)       
            if len(non_zero_factor_list)>= 10 :
                ind = np.argsort(non_zero_factor_list)[::-1][:pareto_value]               
                table_value = sum([non_zero_factor_list[i] for i in ind]) 
                dominant_factors_name_list = [dominant_factors_name_list[i] for i in ind]
            else:
                table_value = sum(non_zero_factor_list)

            ### this is results of the algorithm    
            self.table_value = table_value
            self.dominant_factors_name_list = dominant_factors_name_list         
    
    
####вторая часть расчет несистематической сотавляющей
class Risks:
        def __init__(self,  Rsist):
            self.Rsist= Rsist

        def calculate(self, avs_matrix_values):
            non_zero_count = np.count_nonzero(avs_matrix_values)
            # find non sistematic coefficient value
            self.k = coeff_pairs[non_zero_count][1]
            self.Rnonsist = self.Rsist * self.k
            self.aggregation_risk_value = self.Rsist + self.Rnonsist
            
        




