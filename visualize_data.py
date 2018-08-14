import plotly
import plotly.plotly as py
import plotly.graph_objs as go

class visualize_data():

    def __init__(self):
        plotly.tools.set_credentials_file(username='', api_key='')   #链接云服务器，填写你自己的用户名和api_key

    def bar(self,x,y,name):                             
        trace = go.Bar(x=x,y=y)
        py.iplot([trace],filename=name)

    def pie(self,labels,values,name):                   
        trace = go.Pie(labels=labels,values=values)
        py.iplot([trace],filename=name)
