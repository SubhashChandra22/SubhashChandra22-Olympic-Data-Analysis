from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")
df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://cdn.pixabay.com/photo/2013/02/15/10/58/blue-81847__340.jpg')
#st.dataframe(df)
user_menu=st.sidebar.radio(
    "select the option",('Medal tally','Overall Analysis','Countrywise Analysis','Athlete wise Analysis')
    )

if user_menu=='Medal tally':
    st.sidebar.header("Medal Tally")
    #st.image('https://cdn.pixabay.com/photo/2013/02/15/10/58/blue-81847__340.jpg')
    Country,Years=helper.year_list(df)
    year_selected=st.sidebar.selectbox("Select Year",Years)
    country_selected=st.sidebar.selectbox("Select Country",Country)
    
    medal_tally=helper.fetch_medal_tally(df,year_selected,country_selected)
    
    if year_selected=='Overall' and country_selected=='Overall':
        st.title("Overall Tally ")
    if year_selected!='Overall' and country_selected=='Overall':
        st.title("Medal tally in "+ str(year_selected) +" Olympics")
    if year_selected=='Overall' and country_selected!='Overall':
        st.title(country_selected + "Overall Performanace")
    if year_selected!='Overall' and country_selected!='Overall':
        st.title(country_selected +" Overall perfromance in "+ str(year_selected)+ " Olympics")
    st.table(medal_tally)

if user_menu=="Overall Analysis":
    editions=len(df['Year'].unique())-1
    cities=len(df['City'].unique())
    sports=len(df['Sport'].unique())
    events=len(df['Event'].unique())
    Athletes=len(df['Name'].unique())
    Nations=len(df['region'].unique())
    
    st.header("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col4,col5,col6=st.columns(3)
    with col4:
        st.header("Nations")
        st.title(Nations)
    with col5:
        st.header("Athletes")
        st.title(Athletes)
    with col6:
        st.header("Events")
        st.title(events)
    
    nations_over_time=helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Year", y="region")
    st.title("Particapating Nations Over the Years")
    st.plotly_chart(fig)
    
    events_over_time=helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Year", y="Event")
    st.title("Events Over the Years")
    st.plotly_chart(fig)
    
    Athlets_over_time=helper.data_over_time(df,'Name')
    fig = px.line(Athlets_over_time, x="Year", y="Name")
    st.title("Athletes Over the Years")
    st.plotly_chart(fig)
    
    st.title("Number of events over time(Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)
    
    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)
    
if user_menu=="Countrywise Analysis":
    st.sidebar.title("Country-wise Analysis")
    
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    
    selected_country=st.sidebar.selectbox("Select a country",country_list)
    
    Country_wise =helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(Country_wise, x="Year", y="Medal")
    st.title(selected_country +" Medal Tally Over the Years")
    st.plotly_chart(fig)
    
    st.title(selected_country +" Excellent in Following Events")
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)
    
    st.title("Top 10 Athletes of "+ selected_country )
    top_10_df=helper.most_sucessful_countrywise(df,selected_country)
    st.table(top_10_df)
    
    
if user_menu=='Athlete wise Analysis':
    athlete_df=df.drop_duplicates(['Name','region','Sport'])
    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=800,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)
    
    final=helper.men_vs_women(df)
    st.title("Men vs Female Participation Over Time")
    fig1 = px.line(final, x="Year", y=["Men Participation","Female Participation"])
    fig1.update_layout(autosize=False,width=900,height=600)
    st.plotly_chart(fig1)