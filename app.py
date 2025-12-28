import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# Set page configuration
st.set_page_config(layout="wide")
st.title("North Carolina Interactive Map")

# Load the GeoJSON files using GeoPandas
# Replace the paths with the actual paths to your files
with st.spinner('Loading North Carolina Map Data...'):
    cities_gdf = gpd.read_file("NC_Cities.geojson")
    roads_gdf = gpd.read_file("NC_Roads.geojson")
    counties_gdf = gpd.read_file("NC_Counties.geojson")

# Sidebar for city selection
st.sidebar.header("Navigation")

# Get unique city names from the 'MunicipalB' column
city_list = sorted(cities_gdf['MunicipalB'].unique())
selected_city = st.sidebar.selectbox("Select a City:", city_list)

# Retrieve the county name for the selected city
# The 'CountyName' column in NC_Cities contains the county information
selected_city_data = cities_gdf[cities_gdf['MunicipalB'] == selected_city].iloc[0]
county_name = selected_city_data['CountyName']

# Display the county information on the page
st.subheader(f"Selected City: {selected_city}")
st.write(f"The city of **{selected_city}** is located in **{county_name} County**.")

# Initialize the leafmap
m = leafmap.Map(center=[35.5, -80.0], zoom=7)

# Add the layers to the map
# Adding Counties as the base administrative layer
m.add_gdf(counties_gdf, layer_name="Counties", fill_colors=["#ffffff00"], info_mode='on_hover')

# Adding Roads layer
m.add_gdf(roads_gdf, layer_name="Major Roads", style={'color': 'red', 'weight': 2})

# Highlight the selected city on the map
selected_city_gdf = cities_gdf[cities_gdf['MunicipalB'] == selected_city]
m.add_gdf(selected_city_gdf, layer_name="Selected City", zoom_to_layer=True)

# Display the map in the Streamlit app
from streamlit_folium import st_folium

st_folium(m, width=700, height=500)
