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
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # find_dotenv() method that will try to find a .env file 


GITHUB_TOKEN = os.environ['GITHUB_TOKEN'] 
googleSheetId=os.environ['STREAMLIT_GOOGSHEETID']
workSheetName='Social media posts'
URL=f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={workSheetName}'.replace(" ", "%20")

df=pd.read_csv(URL)
df.fillna(0, inplace=True)
df['date']=pd.to_datetime(df['date'])

# Create regular instagram dataframe
#The Streamlit cache allows your app to execute quickly even when loading data from the web, manipulating large datasets, or performing expensive computations.
@st.cache
def get_data():   
    instagram=df.loc[df['social media'] == 'instagram']   
    return instagram

# Instagram dataframe with 'date' and 'post id' as index
@st.cache
def graph_df():
    instagram=df.loc[df['social media'] == 'instagram']
    graph=instagram.set_index(['date','post id'])
    return graph

# Instagram dataframe with 'date' and 'post id' as index and with specific columns 
@st.cache
def insta_df():
    instagram=df.loc[df['social media'] == 'instagram'].set_index(['date','post id'])
    insta2=instagram[['Likes on posts',
       'Likes on shares', 'Comments on posts', 'Saves on posts',
       'Engagements (likes + comments + shares)','Engagement level (engagements / impressions)',
       'Reach (number of users)', 'Comments on shares', 'Shares on posts',
       'Shares on shares', 'Post link clicks', 'Post unique link clicks',
       'Post other clicks', 'Post unique other clicks', 'Post photo views',
       'Post unique photo views', 'Total post reactions',
       'Post reactions: like', 'Post reactions: love', 'Post reactions: wow',
       'Post reactions: haha', 'Post reactions: sad', 'Post reactions: angry',
       'Post reactions: thankful', 'Post reactions: pride', 'Video views',
       'Total 10s video views', 'Unique video views', 'Autoplay video views',
       'Total 30s video views', 'Unique 30s video views',
       'Auto-played 30s video views', 'Avg. video view time (s)', 'Post exits',
       'Taps forward', 'Taps back']]
    return insta2

# Function return dictionary values
@st.cache
def dictValues():
    insta=insta_df()
    likes_posts = insta[['Likes on posts']]
    likes_shares = insta[['Likes on shares']]
    comments_posts = insta[['Comments on posts']]
    saves_posts = insta[['Saves on posts']]
    engagements = insta[['Engagements (likes + comments + shares)']]
    engagement_level= insta[['Engagement level (engagements / impressions)']]
    reach = insta[['Reach (number of users)']]
    comments_shares= insta[['Comments on shares']]
    shares_posts = insta[['Shares on posts']]
    shares_shares = insta[['Shares on shares']]
    post_link_clicks = insta[['Post link clicks']]
    post_unique_link_clicks = insta[['Post unique link clicks']]
    post_other_clicks = insta[['Post other clicks']]
    post_unique_other_clicks = insta[['Post unique other clicks']]
    post_photo_views = insta[['Post photo views']]
    post_unique_photo_views = insta[['Post unique photo views']]
    total_post_reactions = insta[['Total post reactions']]
    reactions_like = insta[['Post reactions: like']]
    reactions_love = insta[['Post reactions: love']]
    reactions_wow = insta[['Post reactions: wow']]
    reactions_haha = insta[['Post reactions: haha']]
    reactions_sad = insta[['Post reactions: sad']]
    reactions_angry = insta[['Post reactions: angry']]
    reactions_thankful = insta[['Post reactions: thankful']]
    reactions_pride = insta[['Post reactions: pride']]
    video_views = insta[['Video views']]
    total_10s_views = insta[['Total 10s video views']]
    unique_video_views = insta[['Unique video views']]
    autoplay_views = insta[['Autoplay video views']]
    total_30s_views = insta[['Total 30s video views']]
    unique_30s_views = insta[['Unique 30s video views']]
    autoplay_30s_views= insta[['Auto-played 30s video views']]
    avg_video_viewtime = insta[['Avg. video view time (s)']]
    post_exits = insta[['Post exits']]
    taps_forward = insta[['Taps forward']]
    taps_back = insta[['Taps back']]
    return {"Likes on posts": likes_posts,
    "Likes on shares": likes_shares,
    'Comments on posts':comments_posts, 
    'Saves on posts': saves_posts,
    'Engagements (likes + comments + shares)': engagements,
    'Engagement level (engagements / impressions)':engagement_level,
    'Reach (number of users)': reach, 
    'Comments on shares': comments_shares, 
    'Shares on posts': shares_posts,
    'Shares on shares': shares_shares, 
    'Post link clicks': post_link_clicks, 
    'Post unique link clicks': post_unique_link_clicks,
    'Post other clicks': post_other_clicks, 
    'Post unique other clicks': post_unique_other_clicks, 
    'Post photo views':post_photo_views,
    'Post unique photo views':post_unique_photo_views, 
    'Total post reactions':total_post_reactions,
    'Post reactions: like':reactions_like, 
    'Post reactions: love':reactions_love, 
    'Post reactions: wow':reactions_wow,
    'Post reactions: haha':reactions_haha, 
    'Post reactions: sad':reactions_sad, 
    'Post reactions: angry':reactions_angry,
    'Post reactions: thankful': reactions_thankful, 
    'Post reactions: pride': reactions_pride, 
    'Video views': video_views,
    'Total 10s video views':total_10s_views, 
    'Unique video views':unique_video_views, 
    'Autoplay video views':autoplay_views,
    'Total 30s video views':total_30s_views, 
    'Unique 30s video views': unique_30s_views,
    'Auto-played 30s video views':autoplay_30s_views, 
    'Avg. video view time (s)':avg_video_viewtime, 
    'Post exits':post_exits,
    'Taps forward':taps_forward, 
    'Taps back':taps_back}

# Function return dictionary values for popular posts
@st.cache
def topPosts():
    df=get_data()
    df2=df.drop_duplicates(['post id']).copy()
    df2["id_date"] = df.loc[:,"post id"].map(str) + ' ' + df.loc[:,"date"].map(str)
    df2.set_index('id_date', inplace=True)
    
    likes_posts = df2[['Likes on posts']].sort_values(by=['Likes on posts'], ascending=False)
    likes_shares = df2[['Likes on shares']].sort_values(by=['Likes on shares'], ascending=False)
    comments_posts = df2[['Comments on posts']].sort_values(by=['Comments on posts'], ascending=False)
    saves_posts = df2[['Saves on posts']].sort_values(by=['Saves on posts'], ascending=False)
    engagements = df2[['Engagements (likes + comments + shares)']].sort_values(by=['Engagements (likes + comments + shares)'], ascending=False)
    engagement_level= df2[['Engagement level (engagements / impressions)']].sort_values(by=['Engagement level (engagements / impressions)'], ascending=False)
    reach = df2[['Reach (number of users)']].sort_values(by=['Reach (number of users)'], ascending=False)
    comments_shares= df2[['Comments on shares']].sort_values(by=['Comments on shares'], ascending=False)
    shares_posts = df2[['Shares on posts']].sort_values(by=['Shares on posts'], ascending=False)
    shares_shares = df2[['Shares on shares']].sort_values(by=['Shares on shares'], ascending=False)
    post_link_clicks = df2[['Post link clicks']].sort_values(by=['Post link clicks'], ascending=False)
    post_unique_link_clicks = df2[['Post unique link clicks']].sort_values(by=['Post unique link clicks'], ascending=False)
    post_other_clicks = df2[['Post other clicks']].sort_values(by=['Post other clicks'], ascending=False)
    post_unique_other_clicks = df2[['Post unique other clicks']].sort_values(by=['Post unique other clicks'], ascending=False)
    post_photo_views = df2[['Post photo views']].sort_values(by=['Post photo views'], ascending=False)
    post_unique_photo_views = df2[['Post unique photo views']].sort_values(by=['Post unique photo views'], ascending=False)
    total_post_reactions = df2[['Total post reactions']].sort_values(by=['Total post reactions'], ascending=False)
    reactions_like = df2[['Post reactions: like']].sort_values(by=['Post reactions: like'], ascending=False)
    reactions_love = df2[['Post reactions: love']].sort_values(by=['Post reactions: love'], ascending=False)
    reactions_wow = df2[['Post reactions: wow']].sort_values(by=['Post reactions: wow'], ascending=False)
    reactions_haha = df2[['Post reactions: haha']].sort_values(by=['Post reactions: haha'], ascending=False)
    reactions_sad = df2[['Post reactions: sad']].sort_values(by=['Post reactions: sad'], ascending=False)
    reactions_angry = df2[['Post reactions: angry']].sort_values(by=['Post reactions: angry'], ascending=False)
    reactions_thankful = df2[['Post reactions: thankful']].sort_values(by=['Post reactions: thankful'], ascending=False)
    reactions_pride = df2[['Post reactions: pride']].sort_values(by=['Post reactions: pride'], ascending=False)
    video_views = df2[['Video views']].sort_values(by=['Video views'], ascending=False)
    total_10s_views = df2[['Total 10s video views']].sort_values(by=['Total 10s video views'], ascending=False)
    unique_video_views = df2[['Unique video views']].sort_values(by=['Unique video views'], ascending=False)
    autoplay_views = df2[['Autoplay video views']].sort_values(by=['Autoplay video views'], ascending=False)
    total_30s_views = df2[['Total 30s video views']].sort_values(by=['Total 30s video views'], ascending=False)
    unique_30s_views = df2[['Unique 30s video views']].sort_values(by=['Unique 30s video views'], ascending=False)
    autoplay_30s_views= df2[['Auto-played 30s video views']].sort_values(by=['Auto-played 30s video views'], ascending=False)
    avg_video_viewtime = df2[['Avg. video view time (s)']].sort_values(by=['Avg. video view time (s)'], ascending=False)
    post_exits = df2[['Post exits']].sort_values(by=['Post exits'], ascending=False)
    taps_forward = df2[['Taps forward']].sort_values(by=['Taps forward'], ascending=False)
    taps_back = df2[['Taps back']].sort_values(by=['Taps back'], ascending=False)
    return {"Likes on posts": likes_posts,
    "Likes on shares": likes_shares,
    'Comments on posts':comments_posts, 
    'Saves on posts': saves_posts,
    'Engagements (likes + comments + shares)': engagements,
    'Engagement level (engagements / impressions)':engagement_level,
    'Reach (number of users)': reach, 
    'Comments on shares': comments_shares, 
    'Shares on posts': shares_posts,
    'Shares on shares': shares_shares, 
    'Post link clicks': post_link_clicks, 
    'Post unique link clicks': post_unique_link_clicks,
    'Post other clicks': post_other_clicks, 
    'Post unique other clicks': post_unique_other_clicks, 
    'Post photo views':post_photo_views,
    'Post unique photo views':post_unique_photo_views, 
    'Total post reactions':total_post_reactions,
    'Post reactions: like':reactions_like, 
    'Post reactions: love':reactions_love, 
    'Post reactions: wow':reactions_wow,
    'Post reactions: haha':reactions_haha, 
    'Post reactions: sad':reactions_sad, 
    'Post reactions: angry':reactions_angry,
    'Post reactions: thankful': reactions_thankful, 
    'Post reactions: pride': reactions_pride, 
    'Video views': video_views,
    'Total 10s video views':total_10s_views, 
    'Unique video views':unique_video_views, 
    'Autoplay video views':autoplay_views,
    'Total 30s video views':total_30s_views, 
    'Unique 30s video views': unique_30s_views,
    'Auto-played 30s video views':autoplay_30s_views, 
    'Avg. video view time (s)':avg_video_viewtime, 
    'Post exits':post_exits,
    'Taps forward':taps_forward, 
    'Taps back':taps_back}


@st.cache
def df_forIdContentLookup():
    googleSheetId=os.getenv("googsheetid")
    workSheetName='Social media posts'
    URL=f'https://docs.google.com/spreadsheets/d/{googleSheetId}/gviz/tq?tqx=out:csv&sheet={workSheetName}'.replace(" ", "%20")

    df=pd.read_csv(URL)
    df.fillna(0, inplace=True)
    instagram=df.loc[df['social media'] == 'instagram']
    a=instagram.set_index(['post id','date'])
    return a

@st.cache
# Dataframe with column ['post id'] unique values and then set it as index
def df_postID_unique():   
    df=get_data()
    df2=df.drop_duplicates(['post id']).set_index('post id').sort_index()
    
    return df2

# define Panel Visualization Functions

@st.cache(allow_output_mutation=True)
def postAvg_plot():
    """Post Average Calculation"""

    # Convert Google sheet url into CSV format

    instagram=df.loc[df['social media'] == 'instagram']
    instagram=instagram[['date', 'Engagements (likes + comments + shares)', 'Likes on posts','Post unique other clicks','Reach (number of users)','Unique video views', 'social media', 'post id']]
    instagram1 = instagram.groupby('date').agg({'Engagements (likes + comments + shares)' : 'sum',
                                            'Likes on posts' : 'sum',
                                            'Post unique other clicks' : 'sum',
                                            'Reach (number of users)' : 'sum',
                                            'Unique video views' : 'sum',
                                            'post id' : 'nunique' }).reset_index()
    instagram1.rename(columns={"post id": "id_count"},inplace= True)
    instagram1['quotient(sum Engagements (likes + comments + shares)count post id)'] = instagram1['Engagements (likes + comments + shares)'] / instagram1['id_count']
    instagram1['quotient(sum Post unique other clicks count post id)'] = instagram1['Post unique other clicks'] / instagram1['id_count']
    instagram1['quotient(sum Reach (number of users)count post id)'] = instagram1['Reach (number of users)'] / instagram1['id_count']
    instagram1['quotient(sum Unique video views count post id)'] = instagram1['Unique video views'] / instagram1['id_count']
    instagram1['date'] = pd.to_datetime(instagram1['date'])
    instagram1 = instagram1.sort_values('date', ascending= True).reset_index(drop = True)
    visual=instagram1.set_index('date')
    visual.rename(columns={"quotient(sum Engagements (likes + comments + shares)count post id)": "Engagements (likes,comments,share)", "quotient(sum Post unique other clicks count post id)": "Post Unique other clicks", "quotient(sum Reach (number of users)count post id)": "Reach (number of users)count post id", "quotient(sum Unique video views count post id)": "Unique video views count post id"}, inplace=True)
    postavg=visual.drop(columns=[ 'Engagements (likes + comments + shares)', 'Likes on posts',
       'Post unique other clicks', 'Reach (number of users)',
       'Unique video views', 'id_count'])
    
    postavg_plot=postavg.hvplot().opts(title="Post Average Calculation")
    
    return postavg_plot

@st.cache()
def postAvg():
    """Post Average Calculation"""


    instagram=df.loc[df['social media'] == 'instagram']
    instagram=instagram[['date', 'Engagements (likes + comments + shares)', 'Likes on posts','Post unique other clicks','Reach (number of users)','Unique video views', 'social media', 'post id']]
    instagram1 = instagram.groupby('date').agg({'Engagements (likes + comments + shares)' : 'sum',
                                            'Likes on posts' : 'sum',
                                            'Post unique other clicks' : 'sum',
                                            'Reach (number of users)' : 'sum',
                                            'Unique video views' : 'sum',
                                            'post id' : 'nunique' }).reset_index()
    instagram1.rename(columns={"post id": "id_count"},inplace= True)
    instagram1['quotient(sum Engagements (likes + comments + shares)count post id)'] = instagram1['Engagements (likes + comments + shares)'] / instagram1['id_count']
    instagram1['quotient(sum Post unique other clicks count post id)'] = instagram1['Post unique other clicks'] / instagram1['id_count']
    instagram1['quotient(sum Reach (number of users)count post id)'] = instagram1['Reach (number of users)'] / instagram1['id_count']
    instagram1['quotient(sum Unique video views count post id)'] = instagram1['Unique video views'] / instagram1['id_count']
    instagram1['date'] = pd.to_datetime(instagram1['date'])
    instagram1 = instagram1.sort_values('date', ascending= True).reset_index(drop = True)
    visual=instagram1.set_index('date')
    visual.rename(columns={"quotient(sum Engagements (likes + comments + shares)count post id)": "Engagements (likes,comments,share)", "quotient(sum Post unique other clicks count post id)": "Post Unique other clicks", "quotient(sum Reach (number of users)count post id)": "Reach (number of users)count post id", "quotient(sum Unique video views count post id)": "Unique video views count post id"}, inplace=True)
    postavg=visual.drop(columns=[ 'Engagements (likes + comments + shares)', 'Likes on posts',
       'Post unique other clicks', 'Reach (number of users)',
       'Unique video views', 'id_count'])
    return postavg

