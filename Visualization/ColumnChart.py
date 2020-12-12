import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Visualizations import Visualization
from Filter import prepare_dataframe



class ColumnChart(Visualization): 

    def __init__(self, dataframe):
        super().__init__(dataframe)

        #Class varibales with example Parameters
        self.x_encoding = {
            "aggregate": "mean",
            "field": "Sales",
            "type": "quantitative"
        }
        self.y_encoding = {
            "aggregate": None,
            "field": "Country",
            "type": "nominal"
        }

    def normalize_values(self, maxsum):
        if not (self.dataframe_prepared.empty): 
            if self.x_encoding["type"]=="quantitative" : 
                if maxsum == "max":
                    max_value = self.dataframe_prepared[self.x_encoding["field"]].max()
                    min_value = self.dataframe_prepared[self.x_encoding["field"]].min()
                    self.dataframe_prepared[self.x_encoding["field"]] = (self.dataframe_prepared[self.x_encoding["field"]] - min_value) / (max_value - min_value)
                    return self.dataframe_prepared
                elif maxsum == "sum":
                    sum_value = self.dataframe_prepared[self.x_encoding["field"]].sum()
                    min_value = self.dataframe_prepared[self.x_encoding["field"]].min()
                    self.dataframe_prepared[self.x_encoding["field"]] = (self.dataframe_prepared[self.x_encoding["field"]]) / (sum_value)
                    return self.dataframe_prepared

    #def change_axis():
    
    def get_data(self):
        self.dataframe_prepared = prepare_dataframe(self.dataframe,self.y_encoding["field"],self.x_encoding["field"],self.x_encoding["aggregate"])
        return self.dataframe_prepared