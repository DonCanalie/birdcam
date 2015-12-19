# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py # plotly library
import plotly.graph_objs as go

class Climate(object):
    
    def plot(self, recorded, temperature):
                
        data = [
            go.Scatter(
                x=recorded,
                y=temperature
            )
        ]
        
        plot_url = py.plot(data, filename='date-axes')
        
        plot_frame = """<iframe src=\"""" + plot_url + """.embed\"
                            height=\"600\" width=\"100%\"
                            scrolling=\"no\" seamless=\"seamless\"
                            frameBorder=\"0\">
                     </iframe>"""
        plot_frame = "<img src=\"" + plot_url + ".png\">"
        
        return plot_url + ".png"