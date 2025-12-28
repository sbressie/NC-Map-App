import streamlit as st
import geopandas as gpd
import pydeck as pdk

st.set_page_config(layout="wide", page_title="NC City Map")

# 1. Load and Clean Data
@st.cache_data
def load_data():
    cities = gpd.read_file("NC_Cities.geojson")
    roads = gpd.read_file("NC_Roads.geojson")
    counties = gpd.read_file("NC_Counties.geojson")

    return cities, roads, counties

cities_gdf, roads_gdf, counties_gdf = load_data()

# 2. Sidebar Logic
st.sidebar.header("Map Controls")
city_list = sorted(cities_gdf['MunicipalB'].unique())
selected_city = st.sidebar.selectbox("Pick a City:", city_list)

# 3. Report the County (Requirement)
# Find the row for the selected city to get its county
city_data = cities_gdf[cities_gdf['MunicipalB'] == selected_city].iloc[0]
county_name = city_data['CountyName']

st.title(f"Exploring {selected_city}")
st.success(f"📍 The city of **{selected_city}** is located in **{county_name} County**.")

# 4. Define Pydeck Layers
# Layer 1: Counties (Light outlines)
counties_layer = pdk.Layer(
    "GeoJsonLayer",
    counties_gdf,
    get_fill_color=[0, 0, 0, 0], # Transparent fill
    get_line_color=[150, 150, 150], # Grey borders
    line_width_min_pixels=1,
)

# Layer 2: Roads
roads_layer = pdk.Layer(
    "GeoJsonLayer",
    roads_gdf,
    get_line_color=[100, 100, 100, 150],
    get_line_width=200, # Width in meters
    line_width_min_pixels=1,
)

# Layer 3: All Cities (Small grey dots)
cities_layer = pdk.Layer(
    "GeoJsonLayer",
    cities_gdf,
    get_fill_color=[200, 200, 200],
    get_radius=1000,
    point_radius_min_pixels=3,
)

# Layer 4: Selected City (Large blue highlight)
highlight_layer = pdk.Layer(
    "GeoJsonLayer",
    cities_gdf[cities_gdf['MunicipalB'] == selected_city],
    get_fill_color=[0, 128, 255],
    get_radius=3000,
    point_radius_min_pixels=8,
)

# 5. Set the View & Render
# Centers the map on the selected city's coordinates
view_state = pdk.ViewState(
    latitude=city_data.geometry.y,
    longitude=city_data.geometry.x,
    zoom=9,
    pitch=0
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[counties_layer, roads_layer, cities_layer, highlight_layer],
    tooltip={"text": "City: {MunicipalB}\nCounty: {CountyName}"}
))
