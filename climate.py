# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
#
# Example: https://plot.ly/~Dreamshot/2596/temperature-co-2-records-from-vostok-antarctica/

import plotly.plotly as py # plotly library
from plotly.graph_objs import *

class Climate(object):
    
    def plot(self, recorded, temperature, humidity):
                
        data = [
            Scatter(
                x=recorded,
                y=temperature,
                line=Line(
                    color='rgb(153, 0, 255)',
                    shape='linear',
                    width=1
                ),
                name=u'Temperature [\xb0C]',
                uid='46def9',
                visible=True
            ),
	        Scatter(
		        x=recorded,
		        y=humidity,
                line=Line(
                    color='rgb(230, 145, 56)',
                    shape='linear',
                    width=1
                ),
                name='Humidity [%]',
                uid='68e341',
                yaxis='y2'
	        )
        ]
        
        layout = Layout(
            autosize=True,
            #height=650,
            hovermode='x',
            legend=Legend(
                x=1.0418760469011725,
                y=1.0297872340425531,
                bgcolor='rgba(255, 255, 255, 0)'
            ),
            showlegend=True,
            title='Temperature and humidity records',
            #width=900,
#            xaxis=XAxis(
#                autorange=True,
#                mirror=True,
#                #range=[450000, 0],
#                showgrid=False,
#                showline=True,
#                title='<a href="http://birdcam.ddnss.de>birdcam surveillance system</a>',
#                type='linear',
#                zeroline=False
#            ), 
            yaxis=YAxis(
                autorange=True,
                mirror=True,
                #range=[170.01555555555555, 413.70444444444445],
                showgrid=False,
                showline=True,
                title=u'Temperature [\xb0C]',
                titlefont=dict(
                    color='rgb(153, 0, 255)'
                ),
                type='linear',
                zeroline=False
            ),
            yaxis2=YAxis(
                anchor='x',
                autorange=True,
                mirror=True,
                overlaying='y',
                #range=[-10.091111111111111, 16.061446208112876],
                showgrid=False,
                showline=True,
                side='right',
                title='Humidity [%]',
                titlefont=dict(
                    color='rgb(230, 145, 56)'
                ),
                type='linear',
                zeroline=False
            )
        )
        fig = Figure(data=data, layout=layout)
        plot_url = py.plot(fig, filename='date-axes', auto_open=False)
        
        plot_frame = '<iframe src=\"' + plot_url + '.embed\" ' \
                            'height=\"600\" width=\"100%\" ' \
                            'scrolling=\"no\" seamless=\"seamless\" ' \
                            'frameBorder=\"0\">' \
                     '</iframe>'
        
        #return plot_url + ".png"
        return plot_frame