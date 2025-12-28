import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# Use caching so the app stays fast for your mom
@st.cache_data
def load_data():
    # Loading files from your repo
    cities = gpd.read_file("NC_Cities.geojson")
    roads = gpd.read_file("NC_Roads.geojson")
    counties = gpd.read_file("NC_Counties.geojson")
    
    # Fix for common "Timestamp not JSON serializable" error
    for df in [cities, roads, counties]:
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]':
                df[col] = df[col].astype(str)
                
    return cities, roads, counties

cities_gdf, roads_gdf, counties_gdf = load_data()

st.title("North Carolina City Finder")

# Sidebar for selection
st.sidebar.header("Search Settings")
city_list = sorted(cities_gdf['MunicipalB'].unique())
selected_city = st.sidebar.selectbox("Choose a City:", city_list)

# Requirement: Report the county for the picked city
city_info = cities_gdf[cities_gdf['MunicipalB'] == selected_city].iloc[0]
target_county = city_info['CountyName']

st.metric(label="Selected City's County", value=f"{target_county} County")

# Create the Leafmap
m = leafmap.Map(center=[35.5, -79.5], zoom=7)

# Add the layers
m.add_gdf(counties_gdf, layer_name="Counties", fill_colors=["none"], color="blue", weight=1)
m.add_gdf(roads_gdf, layer_name="Roads", style={'color': 'gray', 'weight': 1})

# Highlight only the selected city
selected_city_gdf = cities_gdf[cities_gdf['MunicipalB'] == selected_city]
m.add_gdf(selected_city_gdf, layer_name="Current Location")

# Use st_folium instead of m.to_streamlit() for better stability
st_folium(m, width=1200, height=600, returned_objects=[])
