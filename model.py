
import folium
import pandas as pd
from flask import Flask, render_template



data = pd.read_csv('data.csv')

def find_top_confirmed(num = 20):
    
    top_countries = data.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    count_sort = top_countries.nlargest(num, 'Confirmed')[['Confirmed']]
    return count_sort


corona_df=data.dropna()
m=folium.Map(location=[34.223334,-82.461707],
            tiles='Stamen toner',
            zoom_start=8)
def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],
                 radius=float(x[2])*10,
                 color="red",
                 popup='{}\n confirmed cases:{}'.format(x[3],x[2])).add_to(m)
corona_df[['Lat','Long_','Confirmed','Combined_Key']].apply(lambda x:circle_maker(x),axis=1)
html_map=m._repr_html_()

cdf=find_top_confirmed()
pairs=[(country,confirmed) for country,confirmed in zip(cdf.index,cdf['Confirmed'])]



app=Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html",table = cdf, cmap= html_map,pairs= pairs)


if __name__=="__main__":
    app.run(debug=True)