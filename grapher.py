import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
from datetime import datetime

def plot_graph(df, symbol):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    candles = go.Candlestick(x=df['Datetime'],
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'])
    
    st = go.Scatter(x = df['Datetime'],
                    y = df['ST'],
                    line=dict(color='orange', width=3),
                    name = 'Supertrend')
    
    fig.add_trace(candles)
    fig.add_trace(st,
                 secondary_y=True)
    
    fig.update_layout(title_text=symbol)
    
    fig.show()
    
def update_graph(df, symbol):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    candles = go.Candlestick(x=df['Datetime'],
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'])
    
    st = go.Scatter(x = df['Datetime'],
                    y = df['ST'],
                    line=dict(color='orange', width=3),
                    name = 'Supertrend')
    
    fig.add_trace(candles)
    fig.add_trace(st,
                 secondary_y=True)
    
    fig.update_layout(title_text=symbol)
    
    fig.plotly_update()