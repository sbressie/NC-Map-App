import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# 1. Load the data
@st.cache_data 
def load_data():
    cities = gpd.read_file("NC_Cities.geojson")
    roads = gpd.read_file("NC_Roads.geojson")
    counties = gpd.read_file("NC_Counties.geojson")
    
    return cities, roads, counties

cities_gdf, roads_gdf, counties_gdf = load_data()

# 2. Sidebar City Selection
st.sidebar.title("Settings")
city_list = sorted(cities_gdf['MunicipalB'].unique())
selected_city = st.sidebar.selectbox("Choose a city:", city_list)

# 3. Report the County (Requirement)
city_row = cities_gdf[cities_gdf['MunicipalB'] == selected_city].iloc[0]
county_of_city = city_row['CountyName']

st.title(f"Map of {selected_city}")
st.info(f"📍 {selected_city} is located in **{county_of_city} County**.")

# 4. Create the Map
m = leafmap.Map(center=[35.5, -79.0], zoom=7)

# Add layers
m.add_gdf(counties_gdf, layer_name="Counties", fill_colors=["none"], info_mode=None)
m.add_gdf(roads_gdf, layer_name="Roads", style={'color': 'gray', 'weight': 1})

# Highlight selected city
selected_city_gdf = cities_gdf[cities_gdf['MunicipalB'] == selected_city]
m.add_gdf(selected_city_gdf, layer_name="Selected City")

# 5. Display the Map (The Fix)
st_folium(m, width=1200, height=600, returned_objects=[])
