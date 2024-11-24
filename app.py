# import streamlit as st 
# import pandas as pd 
# import plotly.express as px
import plotly.graph_objects as go
import json
# from copy import deepcopy

# @st.cache_data
# def load_data(path):
#     df = pd.read_csv(path)
#     return df

# # First some Internet Usage Data Exploration
# int_df_row = load_data(path="./data/raw/internet_usages_continent.csv")
# int_df = deepcopy(int_df_row)
# # loading geodata
# with open("./data/raw/countries.geojson", "r") as f:
#     geojson=json.load(f)
# # Add title and header
# st.title("Internet Usage Through 1990 to 2020")
# st.header("Data Exploration")

# # Display the data


      
# #left_column, right_column = st.columns(2)
# left_column, middle_column, right_column = st.columns([3, 1, 1])
 
# years = ["All"]+sorted(pd.unique(int_df['Year']))
# year = left_column.selectbox("Choose a Year", years)
# ##################
# selected=st.select_slider('Select Which Year you want to see ', options=pd.unique(int_df['Year'])) 
# if selected:
#         df_data=int_df[int_df["Year"]==selected]
# #st.table(data=mpg_df)
# if st.checkbox("Show Dataframe"):
#     st.subheader("This is my dataset:")
#     st.dataframe(data=df_data)
    
# #plotly 
# fig1 = px.choropleth_mapbox(df_data,
#                            geojson=geojson,
#                            locations='Entity',  # Replace with your district ID column
#                            color='Internet_usage',  # Column to color the polygons
#                            color_continuous_scale="Viridis",  # Color scale
#                            zoom=0.90,  # Adjust zoom level as needed
#                            featureidkey = "properties.ADMIN",
#                            labels='Year',
#                            center ={"lat": 0, "lon": 0},  # Adjust center coordinates as needed
#                            mapbox_style="carto-positron" , # Mapbox style
#                            hover_name="Entity", hover_data=["Year", "Internet_usage"]
#                            )
# fig1.update_layout(
#     title={"text": "Individuals using the Internet (% of population)", "font": {"size": 24}}
# )
# # fig1.show()
# st.plotly_chart(fig1)
# #show the data in scatter plot
# fig = go.Figure()
# for year in df_data['Year'].unique():
#      ds_aux = df_data[df_data['Year']==year]
#      fig.add_traces(
#         go.Scatter(
#             x=ds_aux['Code'], y=ds_aux['Internet_usage'],
#             mode="markers",
#             name=str(year),
#             marker={"size": ds_aux['Internet_usage'], "sizeref": 2*max(ds_aux['Internet_usage'])/100, "sizemode": "area"},
#             text=ds_aux['Entity'],
#             hovertemplate="<b>%{text}</b><br><br>" +
#                 "Internet Usage Per Person : %{y:.0000f} %<br>" +
#                 f"Year:{year}<br>" +
#                 "<extra></extra>",
#         )
#     )
     
    
# fig.update_layout(title={'text': "Internet Usage", "font": {"size": 24}},
# xaxis={"title": {"text": "Country", "font": {"size": 16}}},
# yaxis={"title": {"text": "Individuals using the Internet (% of population)", "font": {"size": 16}}},)
# st.plotly_chart(fig)
# # fig.show()


# prompt: create streamlit code to build horizontal tab  with thisoptions (All ttime chart, continent chart ,countrychart )

import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data (replace 'internet_usages_continent.csv' with your actual file)
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

# First some Internet Usage Data Exploration
int_df= load_data(path="./data/raw/internet_usages_continent.csv")
# int_df = pd.read_csv("./data/raw/internet_usages_continent.csv")
with open("./data/raw/countries.geojson", "r") as f:
    geojson=json.load(f)

# Create tabs
tab1, tab2, tab3 = st.tabs(["All Time Chart", "Continent Chart", "Country Chart"])
years = ["All"]+sorted(pd.unique(int_df['Year']))
with tab1:
    # All Time Chart content
    # fig = px.line(int_df, x="Year", y="Internet_usage", color="continent", title="Internet Usage per Year by Continent")
    # st.plotly_chart(fig)
    left_column, middle_column, right_column = st.columns([1, 3, 1])
    
    # year = middle_column.selectbox("Choose a Year", years)
    ##################
    selected=st.select_slider('Select Which Year you want to see ', options=pd.unique(int_df['Year'])) 
    if selected:
            df_data=int_df[int_df["Year"]==selected]        
    #plotly 
    fig1 = px.choropleth_mapbox(df_data,
                            geojson=geojson,
                            locations='Entity',  # Replace with your district ID column
                            color='Internet_usage',  # Column to color the polygons
                            color_continuous_scale="Viridis",  # Color scale
                            zoom=0.90,  # Adjust zoom level as needed
                            featureidkey = "properties.ADMIN",
                            # labels='Year',
                            center ={"lat": 0, "lon": 0},  # Adjust center coordinates as needed
                            mapbox_style="carto-positron" , # Mapbox style
                            hover_name="Entity", #hover_data=["Year", "Internet_usage"],
                            hover_data={"Internet_usage": True, "Year": True, "Code": False},
                            labels={'Internet_usage': 'Internet Usage Per Person', 'Year': 'Year'},
                            )
    fig1.update_traces(
        hovertemplate="<b>%{hovertext}</b><br><br>" +
                      "Internet Usage Per Person : %{customdata[0]:.4f} %<br>" +
                      "Year:%{customdata[1]}<br>" +
                      "<extra></extra>")
    fig1.update_layout(
        title={"text": "Individuals using the Internet (% of population)", "font": {"size": 24}}
    )
    # fig1.show()
    st.plotly_chart(fig1)
    #st.table(data=mpg_df)
    if st.checkbox("Show Dataframe"):
        st.subheader("This is the dataset:")
        st.dataframe(data=df_data)

with tab2:
    # Continent Chart content
    continent_year_df = int_df.groupby(['continent', 'Year'])['Internet_usage'].sum().reset_index()
    fig_continent = px.line(continent_year_df, x="Year", y="Internet_usage", color="continent", title="Internet Usage per Year by Continent")
    st.plotly_chart(fig_continent)
    # Create a histogram chart
    fig_continent_hist = px.histogram(continent_year_df, x="continent", y="Internet_usage",
                                     color="continent", histfunc="sum", nbins=10,
                                     title="Total Internet Usage by Continent")

    st.plotly_chart(fig_continent_hist)
with tab3:
    # Country Chart content
    selected_country = st.selectbox("Select a Country", int_df['Entity'].unique())
    df_country = int_df[int_df['Entity'] == selected_country]
    if not df_country.empty:
        fig_country = px.line(df_country, x="Year", y="Internet_usage",  title=f"Internet Usage per Year in  {selected_country}")# +"Internet Usage Per Person : %{y:.0000f} %<br>")
        st.plotly_chart(fig_country)
        fig2 = go.Figure()
        # for year in df_country['Year'].unique():
        ds_aux = df_country#[df_data['Year']==year]
        fig2.add_traces(
            go.Scatter(
                x=ds_aux['Year'], y=ds_aux['Internet_usage'],
                mode="markers",
                # name=str(year),
                marker={"size": ds_aux['Internet_usage'], "sizeref": 2*max(ds_aux['Internet_usage'])/100, "sizemode": "area"},
                text=ds_aux['Entity'],
                hovertemplate="<b>%{text}</b><br><br>" +
                    "Internet Usage Per Person : %{y:.0000f} %<br>" +
                    "Year:%{x}%<br>" +
                    "<extra></extra>",
            )
            )
            
            
        fig2.update_layout(title={'text': "Internet Usage"+selected_country, "font": {"size": 24}},
        xaxis={"title": {"text": "Country", "font": {"size": 16}}},
        yaxis={"title": {"text": "Individuals using the Internet (% of population)", "font": {"size": 16}}},)
        st.plotly_chart(fig2)
        # fig.show()
    else:
        st.write(f"No data available for {selected_country}")