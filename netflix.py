import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


net=pd.read_csv('netflix_titles.csv')
# print(net.head())
net=net.copy()

def movies(net):
    type_movie=net[net['type']=='Movie']
    return(type_movie)

def shows(net):
    return(net[net['type']!='TV show'])

def movies_release(type_movie):

    movie_year=type_movie.groupby('release_year')['show_id'].count().reset_index(name='count')
    movie_year=movie_year[movie_year['release_year']>=2000]
    movie_max=movie_year['count'].max()
    movie_yearmin=movie_year['release_year'].min()
    return(movie_yearmin,movie_max,movie_year)

def show_release(type_shows):
        
    show_year=type_shows.groupby('release_year')['show_id'].count().reset_index(name='count')
    show_year=show_year[show_year['release_year']>=2000]
    show_max=show_year['count'].max()
    return(show_year,show_max)

def bar_movie(movie_year,movie_yearmin,movie_max):

    z=plt.bar(movie_year['release_year'],movie_year['count'],color='black')
    
    plt.xlabel('years')
    plt.ylabel('Number of movie released')
    
    plt.xticks(np.arange(movie_yearmin,2024,1),np.arange(0,24,1))
    plt.yticks(np.arange(0,movie_max,50))
    plt.show()

def bar_shows(show_year,show_max):

    y=plt.bar(show_year['release_year'],show_year['count'],color='black')
    plt.xlabel('years')
    plt.ylabel('Number of shows released')
    plt.show()

# #rate of releasing of movies
def rate_of_movies(net):

    year_analy=net[net['type']=='Movie']
    d=year_analy.groupby('release_year')['type'].count().reset_index(name='count')
    arr=np.array(d['count'])
    diff=0
    for i in range(len(arr)-1):
        diff +=(arr[i+1]-arr[i])

    rate=diff/(len(arr)-1)
    print('average rate of increase in movie is:',rate)

# rate of releasing of movie in particular country
def rate_movie_country(net):

    c=str(input('enter country'))
    year_analy=net[(net['type']=='Movie')&(net['country']==c)]
    d=year_analy.groupby('release_year')['type'].count().reset_index(name='count')
    arr=np.array(d['count'])
    print(arr)
    diff=0
    diff_country=0
    for i in range(len(arr)-1):
        diff_country +=(arr[i+1]-arr[i])

    rate_country=diff/(len(arr)-1)
    print(f'average rate of increase in movie in {c} is:',rate_country)

    # Number of movies in particular gener 
def gener_exploration(net):
    
    net['Geners']=net['listed_in'].str.split(',')  #splitting string into substring and it will become list then separate them in to rows  by explode function giving name as Geners
    net['Geners']=net['Geners'].apply(lambda x: [i.strip() for i in x])
    explod=net.explode('Geners')
    
    return(explod)

def max_genermovie(explod):
    year=int(input("enter year till which you want to analysis:"))
    gener_analy=explod[(explod['release_year']>=year) & (explod['type']=='Movie')]

    gener_analy=gener_analy.groupby('Geners')['show_id'].count().reset_index(name='count')
    gener_analy=gener_analy.sort_values(by=['count'],ascending=True)
    gener_max=gener_analy['count'].max()
    gener_max=gener_analy[gener_analy['count']==gener_max]
    print(f'The most movies are of {gener_max['Geners'].to_string(index=False)} ')
    

def max_genershow(explod):
    year=int(input("enter year till which you want to analysis:"))
    gener_analy=explod[(explod['release_year']<=year) & (explod['type']=='TV Show')]

    gener_analy=gener_analy.groupby('Geners')['show_id'].count().reset_index(name='count')
    gener_analy=gener_analy.sort_values(by=['count'],ascending=True)
    gener_max=gener_analy['count'].max()
    gener_max=gener_analy[gener_analy['count']==gener_max].reset_index(drop=True)
    
    print(f'The most show are of {gener_max['Geners'].to_string(index=False)} ')

def max_gener_peryear_movies(net,explod):
    
    year=net[net['release_year']>2000].release_year.unique()
    year=np.sort(year)
    
    
    max_gener=[]
    max_gener_value=[]
    for i in range(len(year)):
        gener_analy=explod[(explod['release_year']==year[i]) & (explod['type']=='TV Show')]

        gener_analy=gener_analy.groupby('Geners')['show_id'].count().reset_index(name='count')
        gener_analy=gener_analy.sort_values(by=['count'],ascending=True)
        
        gener_max=gener_analy['count'].max()
        
        gener_max=gener_analy[gener_analy['count']==gener_max].reset_index(drop=True)
        
        
        # max_gener.append(gener_max['Geners'].to_string(index=False))
        
        
        value=int(gener_max['count'].values[0])
        
        
        max_gener_value.append(value)
        
    
    plt.bar(year,max_gener_value,color='black')
    plt.show()

def show_upload(net):

    net['date_added']=net['date_added'].str.strip()
    
    net=net.dropna(subset=['date_added']).copy()
    net["date"]=pd.to_datetime(net["date_added"])
    net["months"]=net['date'].dt.month
    # print(net['months'])
    net["year"]=net['date'].dt.year
    # print(net['year'])
    a=net['year'].unique()
    a=a.tolist()
    
    for i in a:
                                                                    
        temp=net[net['year']==i].copy()      
        print(f"for year {i}")
        print(temp.groupby("months")['show_id'].count())
        



 
# type_movie=movies(net)
# type_show=shows(net)
# movie_yearmin,movie_max,movie_year=movies_release(type_movie)
# show_year,show_max=show_release(type_show)
# # bar_movie(movie_year,movie_yearmin,movie_max)
# bar_shows(show_year,show_max)
# rate_of_movies(net)
# explod=gener_exploration(net)
# max_genershow(explod)
# max_genermovie(explod)
# max_gener_peryear_movies(net,explod)
show_upload(net)





