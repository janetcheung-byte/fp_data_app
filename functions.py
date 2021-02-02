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
    
    
    likes_posts = df.groupby(['post id']).agg({'Likes on posts': max, 'date': max }).reset_index()
    likes_posts ["id_date"] = likes_posts.loc[:,"post id"].map(str) + ' ' + likes_posts.loc[:,"date"].map(str)
    likes_posts .set_index('id_date', inplace=True)
    likes_posts .sort_values(by=['Likes on posts'], ascending=False, inplace=True)
    
    
    likes_shares = df.groupby(['post id']).agg({'Likes on shares': max, 'date': max }).reset_index()
    likes_shares ["id_date"] = likes_shares.loc[:,"post id"].map(str) + ' ' + likes_shares.loc[:,"date"].map(str)
    likes_shares.set_index('id_date', inplace=True)
    likes_shares.sort_values(by=['Likes on shares'], ascending=False, inplace=True)
    
    comments_posts = df.groupby(['post id']).agg({'Comments on posts': max, 'date': max }).reset_index()
    comments_posts ["id_date"] = comments_posts.loc[:,"post id"].map(str) + ' ' + comments_posts.loc[:,"date"].map(str)
    comments_posts.set_index('id_date', inplace=True)
    comments_posts.sort_values(by=['Comments on posts'], ascending=False, inplace=True)
    
    saves_posts = df.groupby(['post id']).agg({'Saves on posts': max, 'date': max }).reset_index()
    saves_posts ["id_date"] = saves_posts.loc[:,"post id"].map(str) + ' ' + saves_posts.loc[:,"date"].map(str)
    saves_posts.set_index('id_date', inplace=True)
    saves_posts.sort_values(by=['Saves on posts'], ascending=False, inplace=True) 
    
    engagements = df.groupby(['post id']).agg({'Engagements (likes + comments + shares)': max, 'date': max }).reset_index()
    engagements ["id_date"] = engagements.loc[:,"post id"].map(str) + ' ' + engagements.loc[:,"date"].map(str)
    engagements.set_index('Engagements (likes + comments + shares)', inplace=True)
    engagements.sort_values(by=['Engagements (likes + comments + shares)'], ascending=False, inplace=True)
    
    
    engagement_level = df.groupby(['post id']).agg({'Engagement level (engagements / impressions)': max, 'date': max }).reset_index()
    engagement_level ["id_date"] = engagement_level.loc[:,"post id"].map(str) + ' ' + engagement_level.loc[:,"date"].map(str)
    engagement_level.set_index('Engagement level (engagements / impressions)', inplace=True)
    engagement_level.sort_values(by=['Engagement level (engagements / impressions)'], ascending=False, inplace=True)
    
   
    reach = df.groupby(['post id']).agg({'Reach (number of users)': max, 'date': max }).reset_index()
    reach ["id_date"] = reach.loc[:,"post id"].map(str) + ' ' + reach.loc[:,"date"].map(str)
    reach.set_index('Reach (number of users)', inplace=True)
    reach.sort_values(by=['Reach (number of users)'], ascending=False, inplace=True)
    
    comments_shares = df.groupby(['post id']).agg({'Comments on shares': max, 'date': max }).reset_index()
    comments_shares ["id_date"] = comments_shares.loc[:,"post id"].map(str) + ' ' + comments_shares.loc[:,"date"].map(str)
    comments_shares.set_index('Comments on shares', inplace=True)
    comments_shares.sort_values(by=['Comments on shares'], ascending=False, inplace=True)
    
    shares_posts = df.groupby(['post id']).agg({'Shares on posts': max, 'date': max }).reset_index()
    shares_posts ["id_date"] = shares_posts.loc[:,"post id"].map(str) + ' ' + shares_posts.loc[:,"date"].map(str)
    shares_posts.set_index('Shares on posts', inplace=True)
    shares_posts.sort_values(by=['Shares on posts'], ascending=False, inplace=True)
    
    shares_shares = df.groupby(['post id']).agg({'Shares on shares': max, 'date': max }).reset_index()
    shares_shares ["id_date"] = shares_shares.loc[:,"post id"].map(str) + ' ' + shares_shares.loc[:,"date"].map(str)
    shares_shares.set_index('Shares on shares', inplace=True)
    shares_shares.sort_values(by=['Shares on shares'], ascending=False, inplace=True)
    
    post_link_clicks = df.groupby(['post id']).agg({'Post link clicks': max, 'date': max }).reset_index()
    post_link_clicks ["id_date"] = post_link_clicks.loc[:,"post id"].map(str) + ' ' + post_link_clicks.loc[:,"date"].map(str)
    post_link_clicks.set_index('Post link clicks', inplace=True)
    post_link_clicks.sort_values(by=['Post link clicks'], ascending=False, inplace=True)
    
    post_unique_link_clicks = df.groupby(['post id']).agg({'Post link clicks': max, 'date': max }).reset_index()
    post_unique_link_clicks ["id_date"] = post_unique_link_clicks.loc[:,"post id"].map(str) + ' ' + post_unique_link_clicks.loc[:,"date"].map(str)
    post_unique_link_clicks.set_index('Post link clicks', inplace=True)
    post_unique_link_clicks.sort_values(by=['Post link clicks'], ascending=False, inplace=True)
    
    post_other_clicks = df.groupby(['post id']).agg({'Post other clicks': max, 'date': max }).reset_index()
    post_other_clicks ["id_date"] = post_other_clicks.loc[:,"post id"].map(str) + ' ' + post_other_clicks.loc[:,"date"].map(str)
    post_other_clicks.set_index('Post other clicks', inplace=True)
    post_other_clicks.sort_values(by=['Post other clicks'], ascending=False, inplace=True)
    
    post_unique_other_clicks = df.groupby(['post id']).agg({'Post unique other clicks': max, 'date': max }).reset_index()
    post_unique_other_clicks ["id_date"] = post_unique_other_clicks.loc[:,"post id"].map(str) + ' ' + post_unique_other_clicks.loc[:,"date"].map(str)
    post_unique_other_clicks.set_index('Post unique other clicks', inplace=True)
    post_unique_other_clicks.sort_values(by=['Post unique other clicks'], ascending=False, inplace=True)
    
    post_photo_views = df.groupby(['post id']).agg({'Post photo views': max, 'date': max }).reset_index()
    post_photo_views ["id_date"] = post_photo_views.loc[:,"post id"].map(str) + ' ' + post_photo_views.loc[:,"date"].map(str)
    post_photo_views.set_index('Post photo views', inplace=True)
    post_photo_views.sort_values(by=['Post photo views'], ascending=False, inplace=True)
    
    post_unique_photo_views = df.groupby(['post id']).agg({'Post unique photo views': max, 'date': max }).reset_index()
    post_unique_photo_views ["id_date"] = post_unique_photo_views.loc[:,"post id"].map(str) + ' ' + post_unique_photo_views.loc[:,"date"].map(str)
    post_unique_photo_views.set_index('Post unique photo views', inplace=True)
    post_unique_photo_views.sort_values(by=['Post unique photo views'], ascending=False, inplace=True)
    
    total_post_reactions = df.groupby(['post id']).agg({'Total post reactions': max, 'date': max }).reset_index()
    total_post_reactions ["id_date"] = total_post_reactions.loc[:,"post id"].map(str) + ' ' + total_post_reactions.loc[:,"date"].map(str)
    total_post_reactions.set_index('Total post reactions', inplace=True)
    total_post_reactions.sort_values(by=['Total post reactions'], ascending=False, inplace=True)
    
    reactions_like = df.groupby(['post id']).agg({'Post reactions: like': max, 'date': max }).reset_index()
    reactions_like ["id_date"] = reactions_like.loc[:,"post id"].map(str) + ' ' + reactions_like.loc[:,"date"].map(str)
    reactions_like.set_index('Post reactions: like', inplace=True)
    reactions_like.sort_values(by=['Post reactions: like'], ascending=False, inplace=True)
    
    reactions_love = df.groupby(['post id']).agg({'Post reactions: love': max, 'date': max }).reset_index()
    reactions_love ["id_date"] = reactions_love.loc[:,"post id"].map(str) + ' ' + reactions_love.loc[:,"date"].map(str)
    reactions_love.set_index('Post reactions: love', inplace=True)
    reactions_love.sort_values(by=['Post reactions: love'], ascending=False, inplace=True)
    
    reactions_wow = df.groupby(['post id']).agg({'Post reactions: wow': max, 'date': max }).reset_index()
    reactions_wow ["id_date"] = reactions_wow.loc[:,"post id"].map(str) + ' ' + reactions_wow.loc[:,"date"].map(str)
    reactions_wow.set_index('Post reactions: wow', inplace=True)
    reactions_wow.sort_values(by=['Post reactions: wow'], ascending=False, inplace=True)
     
    reactions_haha = df.groupby(['post id']).agg({'Post reactions: haha': max, 'date': max }).reset_index()
    reactions_haha ["id_date"] = reactions_haha.loc[:,"post id"].map(str) + ' ' + reactions_haha.loc[:,"date"].map(str)
    reactions_haha.set_index('Post reactions: haha', inplace=True)
    reactions_haha.sort_values(by=['Post reactions: haha'], ascending=False, inplace=True)
                                                         
                              
    reactions_sad = df.groupby(['post id']).agg({'Post reactions: sad': max, 'date': max }).reset_index()
    reactions_sad ["id_date"] = reactions_sad.loc[:,"post id"].map(str) + ' ' + reactions_sad.loc[:,"date"].map(str)
    reactions_sad.set_index('Post reactions: sad', inplace=True)
    reactions_sad.sort_values(by=['Post reactions: sad'], ascending=False, inplace=True)
                                                          
    reactions_angry = df.groupby(['post id']).agg({'Post reactions: angry': max, 'date': max }).reset_index()
    reactions_angry ["id_date"] = reactions_angry.loc[:,"post id"].map(str) + ' ' + reactions_angry.loc[:,"date"].map(str)
    reactions_angry.set_index('Post reactions: angry', inplace=True)
    reactions_angry.sort_values(by=['Post reactions: angry'], ascending=False, inplace=True)
                              
    
    reactions_thankful = df.groupby(['post id']).agg({'Post reactions: thankful': max, 'date': max }).reset_index()
    reactions_thankful ["id_date"] = reactions_thankful.loc[:,"post id"].map(str) + ' ' + reactions_thankful.loc[:,"date"].map(str)
    reactions_thankful.set_index('Post reactions: thankful', inplace=True)
    reactions_thankful.sort_values(by=['Post reactions: thankful'], ascending=False, inplace=True)
                                
    reactions_pride = df.groupby(['post id']).agg({'Post reactions: pride': max, 'date': max }).reset_index()
    reactions_pride ["id_date"] = reactions_pride.loc[:,"post id"].map(str) + ' ' + reactions_pride.loc[:,"date"].map(str)
    reactions_pride.set_index('Post reactions: pride', inplace=True)
    reactions_pride.sort_values(by=['Post reactions: pride'], ascending=False, inplace=True)
                                                              
    video_views = df.groupby(['post id']).agg({'Video views': max, 'date': max }).reset_index()
    video_views ["id_date"] = video_views.loc[:,"post id"].map(str) + ' ' + video_views.loc[:,"date"].map(str)
    video_views.set_index('Video views', inplace=True)
    video_views.sort_values(by=['Video views'], ascending=False, inplace=True)
                                                       
    total_10s_views = df.groupby(['post id']).agg({'Video views': max, 'date': max }).reset_index()
    total_10s_views ["id_date"] = total_10s_views.loc[:,"post id"].map(str) + ' ' + total_10s_views.loc[:,"date"].map(str)
    total_10s_views.set_index('Video views', inplace=True)
    total_10s_views.sort_values(by=['Video views'], ascending=False, inplace=True)
                                                       
    unique_video_views = df.groupby(['post id']).agg({'Unique video views': max, 'date': max }).reset_index()
    unique_video_views ["id_date"] = unique_video_views.loc[:,"post id"].map(str) + ' ' + unique_video_views.loc[:,"date"].map(str)
    unique_video_views.set_index('Unique video views', inplace=True)
    unique_video_views.sort_values(by=['Unique video views'], ascending=False, inplace=True)
                                                              
    autoplay_views = df.groupby(['post id']).agg({'Autoplay video views': max, 'date': max }).reset_index()
    autoplay_views ["id_date"] = autoplay_views.loc[:,"post id"].map(str) + ' ' + autoplay_views.loc[:,"date"].map(str)
    autoplay_views.set_index('Autoplay video views', inplace=True)
    autoplay_views.sort_values(by=['Autoplay video views'], ascending=False, inplace=True)
                                                              
    total_30s_views = df.groupby(['post id']).agg({'Total 30s video views': max, 'date': max }).reset_index()
    total_30s_views ["id_date"] = total_30s_views.loc[:,"post id"].map(str) + ' ' + total_30s_views.loc[:,"date"].map(str)
    total_30s_views.set_index('Total 30s video views', inplace=True)
    total_30s_views.sort_values(by=['Total 30s video views'], ascending=False, inplace=True)
                               
                             
    unique_30s_views = df.groupby(['post id']).agg({'Unique 30s video views': max, 'date': max }).reset_index()
    unique_30s_views ["id_date"] = unique_30s_views.loc[:,"post id"].map(str) + ' ' + unique_30s_views.loc[:,"date"].map(str)
    unique_30s_views.set_index('Unique 30s video views', inplace=True)
    unique_30s_views.sort_values(by=['Unique 30s video views'], ascending=False, inplace=True)
                                                           
    autoplay_30s_views = df.groupby(['post id']).agg({'Auto-played 30s video views': max, 'date': max }).reset_index()
    autoplay_30s_views ["id_date"] = autoplay_30s_views.loc[:,"post id"].map(str) + ' ' + autoplay_30s_views.loc[:,"date"].map(str)
    autoplay_30s_views.set_index('Auto-played 30s video views', inplace=True)
    autoplay_30s_views.sort_values(by=['Auto-played 30s video views'], ascending=False, inplace=True)
                                                                 
    avg_video_viewtime = df.groupby(['post id']).agg({'Avg. video view time (s)': max, 'date': max }).reset_index()
    avg_video_viewtime ["id_date"] = avg_video_viewtime.loc[:,"post id"].map(str) + ' ' + avg_video_viewtime.loc[:,"date"].map(str)
    avg_video_viewtime.set_index('Avg. video view time (s)', inplace=True)
    avg_video_viewtime.sort_values(by=['Avg. video view time (s)'], ascending=False, inplace=True)
                                   
                              
    post_exits = df.groupby(['post id']).agg({'Post exits': max, 'date': max }).reset_index()
    post_exits ["id_date"] = post_exits.loc[:,"post id"].map(str) + ' ' + post_exits.loc[:,"date"].map(str)
    post_exits.set_index('Post exits', inplace=True)
    post_exits.sort_values(by=['Post exits'], ascending=False, inplace=True)
                                                         
    taps_forward = df.groupby(['post id']).agg({'Taps forward': max, 'date': max }).reset_index()
    taps_forward ["id_date"] = taps_forward.loc[:,"post id"].map(str) + ' ' + taps_forward.loc[:,"date"].map(str)
    taps_forward.set_index('Taps forward', inplace=True)
    taps_forward.sort_values(by=['Taps forward'], ascending=False, inplace=True)
                               
                             
    taps_back = df.groupby(['post id']).agg({'Taps back': max, 'date': max }).reset_index()
    taps_back ["id_date"] = taps_back.loc[:,"post id"].map(str) + ' ' + taps_back.loc[:,"date"].map(str)
    taps_back.set_index('Taps back', inplace=True)
    taps_back.sort_values(by=['Taps back'], ascending=False, inplace=True)
                             
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

@st.cache()
def pctChange():
    insta5=df.loc[df['social media'] == 'instagram']
    insta5=insta5[['Likes on posts','post id','date']].copy()
    insta5=insta5.pivot_table(index=['post id','date'])
    insta5['pct_change']=insta5['Likes on posts'].pct_change()*100
    insta5.dropna(inplace=True)
    insta5[['pct_change']]
    plot=insta5[['pct_change']]
    return plot