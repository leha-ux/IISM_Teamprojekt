import os
import sys
import json
import requests

sys.path.append(os.path.join(".", os.path.dirname(os.path.abspath(__file__)), "Visualization"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Filter import prepare_dataframe, calculate_theta, final_prep
from BarChart import BarChart
from ColumnChart import ColumnChart
from PieChart import PieChart
from ScatterPlot import ScatterPlot
from VisHandler import VisHandler
from flask import Flask, jsonify, request
from flask_cors import CORS
from nl4dv import NL4DV
from nl4dv_parser import nl4dv_output_parser
from jsonPrinter import jsonPrettyPrinter

#NL4DV
def nl4dvQueryAnalyzerFinancialsDataset(query) :
    full_path = os.path.abspath(__file__)
    nl4dv_instance = NL4DV(data_url = os.path.join(".", os.path.dirname(os.path.abspath(__file__)), "examples", "assets", "data", "FinancialSample.csv"))
    dependency_parser_config = {"name": "corenlp", "model": os.path.join(".", os.path.dirname(os.path.abspath(__file__)), "examples","assets","jars","stanford-english-corenlp-2018-10-05-models.jar"),"parser": os.path.join(".", os.path.dirname(os.path.abspath(__file__)), "examples","assets","jars","stanford-parser.jar")}
    nl4dv_instance.set_dependency_parser(config=dependency_parser_config)
    queryInput = query
    return nl4dv_instance.analyze_query(queryInput)

#test data
keywords = {"Country": ["in", ["France", "Canada"]], "Segment": ["in", ["Government", "Enterprise"]]}
x_encoding = {"field": "Country", "type": "quantitative"}
y_encoding = {"aggregate":"sum", "field": "Sales", "type": "quantitative"}


#Import XLXS Data
#working_dataframe = pd.read_csv(os.path.join(".", os.path.dirname(os.path.abspath(__file__)), "examples", "assets", "data", "FinancialSample.csv"))
working_dataframe = pd.read_excel(os.path.join(".", os.path.dirname(os.path.abspath(__file__)), "examples", "assets", "data", "FinancialSample.xlsx"), engine='openpyxl')


#create and modify Objects
b1 = BarChart(working_dataframe, x_encoding, y_encoding, keywords)
final_vis =  VisHandler(b1)
#final_vis.vis_object.set_aggregate(None, "mean")



#configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


#"main"
@app.route('/nl4dv', methods=['GET', 'POST'])
def nl4dv_query():
    post_data = request.get_json()
    nl4dv_results = (nl4dvQueryAnalyzerFinancialsDataset(post_data["query"]))
    return jsonify(nl4dv_results)

@app.route('/data', methods=['GET'])
def all_data():
    return final_vis.jsonify_vis()


if __name__ == '__main__':
    app.run()