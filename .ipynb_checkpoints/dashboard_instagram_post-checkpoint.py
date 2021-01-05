# import libraries
import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import hvplot.pandas
import panel as pn
import plotly.express as px
from pathlib import Path
import holoviews as hv
import hvplot.pandas
import seaborn as sns
import functions as f
import numpy as np



# create dataframe instance
df = f.get_data()
graph=f.graph_df()
idContent=f.df_postID_unique()

# Options to show dataframe
if st.checkbox('Show dataframe'):
    st.dataframe(df.style.highlight_max(axis=0))
      
    
# See post id content
if st.checkbox('Show Post ID content'):
    values = idContent.index.to_list()
    options = idContent['Post caption'].tolist()
    dic = dict(zip(options, values))
    a=st.selectbox('Choose a post id', options, format_func=lambda x: dic[x])
    st.write(a)
    
        
# Select dataframe column names to produce visual graph 
if st.checkbox('Select your chart'):
    plots = f.dictValues()
    plot = st.selectbox("Select your chart.", list(plots.keys()))
    'You selected: ', plot
    st.write(hv.render(plots[plot].hvplot(kind='bar',x='date',by='post id', stacked=True, rot=90, use_container_width=True, width=2000, height=1000), backend='bokeh'))# Visual graph

# Post average calculation visual graph
if st.checkbox('Show Post Average Calculation '):
    st.write(hv.render(f.postAvg().hvplot(kind='line',x='date', rot=90, use_container_width=True, title="Post Average Calculation"), backend='bokeh'))
    
