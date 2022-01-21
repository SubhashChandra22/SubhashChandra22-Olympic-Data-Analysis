from ast import fix_missing_locations
import pandas as pd

def fetch_medal_tally(df,year,country):
    flag=0
    medal_df=df.drop_duplicates(subset=['Team',"NOC",'Games','Season','City','Sport','Event','Medal','region'])
    
    if (year=='Overall' and country=='Overall'):
        temp_df=medal_df

    if (year=='Overall' and country!='Overall'):
        flag=1
        temp_df=medal_df[medal_df['region']==country]
         
    if(year!='Overall' and country=='Overall'):
       temp_df = medal_df[medal_df['Year'] == int(year)]

    if(year!='Overall' and country!='Overall'):
        temp_df=medal_df[(medal_df['Year']==year) & (medal_df['region']==country)]

    if flag==1:
        x=temp_df.groupby('Year')[['Gold','Silver','Bronze']].sum().sort_values('Year',ascending=False).reset_index()
    else:
        x=temp_df.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')


    return x



def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team',"NOC",'Games','Season','City','Sport','Event','Medal','region'])
    medal_tally=medal_tally.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['Total']=medal_tally['Total'].astype('int')
    return medal_tally


def year_list(df):
    Year=df['Year'].unique().tolist()
    Year.sort()
    Year.insert(0,"Overall")

    Country=df['region'].dropna().unique().tolist()
    Country.sort()
    Country.insert(0,"Overall")
    return Country,Year

def data_over_time(df,col):
    nations_over_time=df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index().sort_values(by=['index'])
    nations_over_time.rename(columns={'index':'Year','Year':col},inplace=True)
    return nations_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team',"NOC",'Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year')['Medal'].count().reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team',"NOC",'Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_sucessful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])


    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def men_vs_women(df):
    athlete_df=df.drop_duplicates(['Name','region','Event','Sport'])
    men=athlete_df[athlete_df['Sex']=="M"].groupby("Year")['Sex'].count().reset_index()
    men.rename(columns={"Sex":"Men Participation"},inplace=True)
    female=athlete_df[athlete_df['Sex']=="F"].groupby("Year")['Sex'].count().reset_index()
    female.rename(columns={"Sex":"Female Participation"},inplace=True)
    final=men.merge(female,how='left').fillna(0)
    return final