import streamlit as st
import geopandas as gpd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static

st.set_page_config(layout="wide")
st.title("North Carolina Kepler.gl Visualization")

@st.cache_data
def load_data():
    # Loading your specific GeoJSON files
    cities = gpd.read_file("NC_Cities.geojson")
    roads = gpd.read_file("NC_Roads.geojson")
    counties = gpd.read_file("NC_Counties.geojson")
    
    # Cleaning Timestamp columns (found in NC_Cities) for JSON compatibility
    for df in [cities, roads, counties]:
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]' or 'date' in col.lower():
                df[col] = df[col].astype(str)
    
    return cities, roads, counties

cities_gdf, roads_gdf, counties_gdf = load_data()

# Requirement: Report the county for a selected city
city_list = sorted(cities_gdf['MunicipalB'].unique())
selected_city = st.sidebar.selectbox("Choose a City:", city_list)
city_row = cities_gdf[cities_gdf['MunicipalB'] == selected_city].iloc[0]
st.sidebar.write(f"**County:** {city_row['CountyName']}")

# Create the Kepler.gl Map
# We pass the data in a dictionary format
map_1 = KeplerGl(height=600)
map_1.add_data(data=counties_gdf, name="NC Counties")
map_1.add_data(data=roads_gdf, name="NC Roads")
map_1.add_data(data=cities_gdf[cities_gdf['MunicipalB'] == selected_city], name="Selected City")

# Display the map in Streamlit
keplergl_static(map_1)
