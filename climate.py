# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
#
# TODO: Zwei y-Achsen implementieren https://plot.ly/~Dreamshot/2596/temperature-co-2-records-from-vostok-antarctica/

import plotly.plotly as py # plotly library
import plotly.graph_objs as go

class Climate(object):
    
    def plot(self, recorded, temperature, humidity):
                
        data = [
            go.Scatter(
                x=recorded,
                y=temperature
            ),
	    go.Scatter(
		x=recorded,
		y=humidity
	    )
        ]
        
        plot_url = py.plot(data, filename='date-axes', auto_open=False)
        
        plot_frame = """<iframe src=\"""" + plot_url + """.embed\"
                            height=\"600\" width=\"100%\"
                            scrolling=\"no\" seamless=\"seamless\"
                            frameBorder=\"0\">
                     </iframe>"""
        plot_frame = "<img src=\"" + plot_url + ".png\">"
        
        return plot_url + ".png"
