import streamlit as st 
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

# First some Internet Usage Data Exploration
int_df_row = load_data(path="./data/raw/internet_usages.csv")
int_df = deepcopy(int_df_row)
# loading geodata
with open("./data/raw/countries.geojson", "r") as f:
    geojson=json.load(f)
# Add title and header
st.title("Internet Usage Through 1990 to 2020")
st.header("Data Exploration")




      
#left_column, right_column = st.columns(2)
left_column, middle_column, right_column = st.columns([3, 1, 1])
 
years = ["All"]+sorted(pd.unique(int_df['Year']))
year = left_column.selectbox("Choose a Year", years)
##################
selected=st.select_slider('Select Which Year you want to see ', options=pd.unique(int_df['Year'])) 
if selected:
        df_data=int_df[int_df["Year"]==selected]
#st.table(data=mpg_df)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=df_data)
    
#plotly 
fig1 = px.choropleth_mapbox(df_data,
                           geojson=geojson,
                           locations='Entity',  # Replace with your district ID column
                           color='Internet_usage',  # Column to color the polygons
                           color_continuous_scale="Viridis",  # Color scale
                           zoom=0.90,  # Adjust zoom level as needed
                           featureidkey = "properties.ADMIN",
                           labels='Year',
                           center ={"lat": 0, "lon": 0},  # Adjust center coordinates as needed
                           mapbox_style="carto-positron" , # Mapbox style
                           hover_name="Entity", hover_data=["Year", "Internet_usage"]
                           )
fig1.update_layout(
    title={"text": "Individuals using the Internet (% of population)", "font": {"size": 24}}
)
# fig1.show()
st.plotly_chart(fig1)
#show the data in scatter plot
fig = go.Figure()
for year in df_data['Year'].unique():
     ds_aux = df_data[df_data['Year']==year]
     fig.add_traces(
        go.Scatter(
            x=ds_aux['Code'], y=ds_aux['Internet_usage'],
            mode="markers",
            name=str(year),
            marker={"size": ds_aux['Internet_usage'], "sizeref": 2*max(ds_aux['Internet_usage'])/100, "sizemode": "area"},
            text=ds_aux['Entity'],
            hovertemplate="<b>%{text}</b><br><br>" +
                "Internet Usage Per Person : %{y:.0000f} %<br>" +
                f"Year:{year}<br>" +
                "<extra></extra>",
        )
    )
     
    
fig.update_layout(title={'text': "Internet Usage", "font": {"size": 24}},
xaxis={"title": {"text": "Country", "font": {"size": 16}}},
yaxis={"title": {"text": "Individuals using the Internet (% of population)", "font": {"size": 16}}},)
st.plotly_chart(fig)
# fig.show()