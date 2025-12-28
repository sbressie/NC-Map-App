import streamlit as st
import geopandas as gpd
import pydeck as pdk

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    cities = gpd.read_file("NC_Cities.geojson")
    counties = gpd.read_file("NC_Counties.geojson")
    roads = gpd.read_file("NC_Roads.geojson")

    return cities, counties, roads

cities_gdf, counties_gdf, roads_gdf = load_data()

# Sidebar: City Selection & Census Info
st.sidebar.header("City Selection")
selected_city = st.sidebar.selectbox("Select a City:", sorted(cities_gdf['MunicipalB'].unique()))

# Retrieve specific data points for the selected city
city_info = cities_gdf[cities_gdf['MunicipalB'] == selected_city].iloc[0]

st.sidebar.subheader(f"Census Data for {selected_city}")
st.sidebar.write(f"**Census Type:** {city_info['CensusType']}")
st.sidebar.write(f"**Census Population:** {city_info['CensusPopu']:,}")
st.sidebar.write(f"**Census Year:** {city_info['CensusYear']}")

# Map Layout
st.title(f"NC Map: {selected_city} in {city_info['CountyName']} County")

# Define Layers
# Counties styled in Light Pink
counties_layer = pdk.Layer(
    "GeoJsonLayer",
    counties_gdf,
    get_fill_color=[255, 182, 193, 100],  # Light Pink (RGBA)
    get_line_color=[255, 105, 180],       # Hot Pink border
    line_width_min_pixels=1,
)

roads_layer = pdk.Layer(
    "GeoJsonLayer",
    roads_gdf,
    get_line_color=[120, 120, 120],
    line_width_min_pixels=1,
)

city_highlight = pdk.Layer(
    "GeoJsonLayer",
    cities_gdf[cities_gdf['MunicipalB'] == selected_city],
    get_fill_color=[255, 0, 0],
    get_radius=2000,
    point_radius_min_pixels=8,
)

# Viewport centered on the selected city
view_state = pdk.ViewState(
    latitude=city_info.geometry.y,
    longitude=city_info.geometry.x,
    zoom=10,
    pitch=0
)

# Render the Map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[counties_layer, roads_layer, city_highlight],
    tooltip={"text": "City: {MunicipalB}\nCensus Pop: {CensusPopu}"}
))
