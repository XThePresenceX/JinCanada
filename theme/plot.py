import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import requests
import json

def get_graph(): 
    def get_json(url):
        response = requests.get(url)
        rows = json.loads(response.text)['rounds']
        data = pd.DataFrame.from_dict(rows)
        filteredColums = data[["drawNumber", "drawDate", "drawName", "drawCRS"]]
        filteredRows = filteredColums[(filteredColums['drawName'] == "No Program Specified") | (filteredColums['drawName'] == "Canadian Experience Class")]
        return filteredRows

    immigrationData = get_json("https://www.canada.ca/content/dam/ircc/documents/json/ee_rounds_123_en.json#/classes")
    filteredGraph = immigrationData[["drawCRS", "drawDate"]]
    filteredGraph.drawDate = pd.to_datetime(filteredGraph['drawDate'])
    filteredGraph.drawCRS = pd.to_numeric(filteredGraph['drawCRS'])

    fig = go.Figure(data=go.Scatter(x=filteredGraph.drawDate, y=filteredGraph.drawCRS))
    fig.update_layout(title='Express Entry (CEC) score (2015-Now)', xaxis_title='Date of Draw', yaxis_title='CRS Score')
    fig.update_traces(mode='lines+markers')
    # fig.show()
    fig.write_html("plot.html")


get_graph()
# date_array  = filteredGraph['drawDate']
# crs_array = filteredGraph['drawCRS']
# print(date_array)
# print(crs_array)
