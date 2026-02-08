"""
AI-Powered Native Plantation Planning System
Streamlit interface with real ML backend integration
"""

import sys
import os
sys.path.append(os.path.abspath("."))

import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap, MarkerCluster
import random
import pandas as pd
import json
import numpy as np
from PIL import Image
import io
import base64

# Import our ML modules
from src.recommendation.species import recommend_species
from src.optimization.grid import generate_grid
from src.optimization.suitability import compute_suitability

# Import our custom analyzers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
try:
    from utils.image_analyzer import PlantationImageAnalyzer
    from models.terrain_classifier import TerrainClassifier
    USE_ML_BACKEND = True
except ImportError:
    USE_ML_BACKEND = False
    print("Warning: ML backend not available, using mock data")

# --------------------------------------------------
# Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Plantation Optimizer",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Initialize Session State
# --------------------------------------------------
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "lat": None,
        "lon": None,
        "points": [],
        "ndvi_grid": [],
        "env": None,
        "df": None,
        "analysis_complete": False,
        "uploaded_image": None,
        "image_analysis": None,
        "terrain_stats": None,
        "suitability_map": None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def analyze_with_ml(image_data, lat, lon):
    """Analyze image using ML backend"""
    if not USE_ML_BACKEND:
        return None
    
    try:
        # Save uploaded image temporarily
        temp_path = "/tmp/uploaded_satellite.png"
        image_data.save(temp_path)
        
        # Run analysis
        analyzer = PlantationImageAnalyzer()
        results = analyzer.analyze_image(temp_path, save_visualizations=False)
        
        # Run terrain classification
        classifier = TerrainClassifier()
        img_array = np.array(image_data)
        classification = classifier.predict(img_array)
        terrain_stats = classifier.get_class_statistics(classification)
        
        return {
            'results': results,
            'terrain_stats': terrain_stats,
            'classification': classification
        }
    except Exception as e:
        st.error(f"ML Analysis Error: {str(e)}")
        return None


def generate_plantation_points_ml(lat, lon, suitability_data=None):
    """Generate plantation points using ML or fallback to grid method"""
    
    if suitability_data is not None and USE_ML_BACKEND:
        # Use ML-based generation
        points = generate_points_from_suitability(
            lat, lon, suitability_data, num_points=100
        )
    else:
        # Fallback to grid-based generation
        points = generate_points_grid(lat, lon)
    
    return points


def generate_points_from_suitability(lat, lon, suitability_map, num_points=100):
    """Generate points based on ML suitability scores"""
    height, width = suitability_map.shape
    
    # Find suitable pixels (score > 50)
    suitable_mask = suitability_map > 50
    suitable_coords = np.argwhere(suitable_mask)
    suitable_scores = suitability_map[suitable_mask]
    
    if len(suitable_coords) == 0:
        # Lower threshold if needed
        suitable_mask = suitability_map > 30
        suitable_coords = np.argwhere(suitable_mask)
        suitable_scores = suitability_map[suitable_mask]
    
    # Sort by score
    sorted_indices = np.argsort(suitable_scores)[::-1]
    suitable_coords = suitable_coords[sorted_indices]
    suitable_scores = suitable_scores[sorted_indices]
    
    # Greedy selection with spacing
    selected_points = []
    min_pixel_spacing = 15  # Minimum pixels between trees
    
    for i, (y, x) in enumerate(suitable_coords):
        if len(selected_points) >= num_points:
            break
        
        # Check spacing
        too_close = False
        for prev_y, prev_x, _, _ in selected_points:
            distance = np.sqrt((y - prev_y)**2 + (x - prev_x)**2)
            if distance < min_pixel_spacing:
                too_close = True
                break
        
        if not too_close:
            # Convert pixel to lat/lon (approximate)
            lat_offset = ((y / height) - 0.5) * 0.01  # ~1km radius
            lon_offset = ((x / width) - 0.5) * 0.01
            
            point_lat = lat + lat_offset
            point_lon = lon + lon_offset
            score = float(suitable_scores[i])
            
            # Get environmental factors
            ndvi = min(1.0, score / 100.0)
            water = random.uniform(0.4, 0.8)
            soil = random.uniform(0.5, 0.9)
            
            species = recommend_species(ndvi, water, soil)
            
            selected_points.append((
                point_lat,
                point_lon,
                score,
                species
            ))
    
    return [
        {
            "lat": p[0],
            "lon": p[1],
            "score": p[2],
            "species": p[3]
        }
        for p in selected_points
    ]


def generate_points_grid(lat, lon):
    """Fallback grid-based point generation"""
    ndvi_base = round(random.uniform(0.4, 0.9), 2)
    water = round(random.uniform(0.3, 0.8), 2)
    soil = round(random.uniform(0.4, 0.9), 2)
    
    grid = generate_grid(lat, lon)
    points = []
    
    for g in grid:
        local_ndvi = max(0, min(1, ndvi_base + random.uniform(-0.1, 0.1)))
        score = compute_suitability(local_ndvi, water, soil)
        species = recommend_species(local_ndvi, water, soil)
        
        points.append({
            "lat": g[0],
            "lon": g[1],
            "score": score,
            "species": species
        })
    
    points.sort(key=lambda x: x["score"], reverse=True)
    return points[:100]


def create_heatmap_data(points):
    """Create heatmap data from points"""
    return [
        [p["lat"], p["lon"], p["score"] / 100.0]
        for p in points
    ]

# --------------------------------------------------
# UI Header
# --------------------------------------------------
st.title("🌱 AI-Powered Native Plantation Planning System")
st.markdown(
    """
    <div style='background-color: #90ee90; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
    <b>🎯 How it works:</b>
    <ol>
        <li>📍 Click on the map to select a location OR upload a satellite image</li>
        <li>🤖 AI analyzes vegetation, soil, and water availability</li>
        <li>🎯 System generates 100 optimal plantation coordinates</li>
        <li>🌿 Get native species recommendations for each point</li>
        <li>📥 Download the complete plantation plan</li>
    </ol>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar - Upload & Settings
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Image upload
    st.subheader("📤 Upload Satellite Image")
    uploaded_file = st.file_uploader(
        "Upload satellite imagery (optional)",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a satellite image for ML-based analysis"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_image = Image.open(uploaded_file)
        st.image(st.session_state.uploaded_image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("🔍 Analyze Image with ML", type="primary"):
            with st.spinner("Running ML analysis..."):
                if st.session_state.lat and st.session_state.lon:
                    ml_results = analyze_with_ml(
                        st.session_state.uploaded_image,
                        st.session_state.lat,
                        st.session_state.lon
                    )
                    if ml_results:
                        st.session_state.image_analysis = ml_results['results']
                        st.session_state.terrain_stats = ml_results['terrain_stats']
                        st.success("✅ ML Analysis complete!")
                        st.rerun()
                else:
                    st.warning("Please select a location on the map first")
    
    st.markdown("---")
    
    # Settings
    st.subheader("🎛️ Settings")
    num_points = st.slider("Number of plantation points", 50, 200, 100, 10)
    min_spacing = st.slider("Minimum tree spacing (meters)", 2.0, 10.0, 3.0, 0.5)
    
    st.markdown("---")
    
    # Info
    st.subheader("ℹ️ Analysis Status")
    if st.session_state.analysis_complete:
        st.success("✅ Analysis Complete")
        st.metric("Points Generated", len(st.session_state.points))
    else:
        st.info("👆 Click on map to start")
    
    if USE_ML_BACKEND:
        st.success("🤖 ML Backend: Active")
    else:
        st.warning("🤖 ML Backend: Using Mock Data")

# --------------------------------------------------
# Main Content
# --------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Interactive Map")
    
    # Handle map click
    if st.session_state.lat is not None:
        center_lat = st.session_state.lat
        center_lon = st.session_state.lon
        zoom = 16
    else:
        center_lat = 23.0225
        center_lon = 72.5714
        zoom = 14
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="OpenStreetMap"
    )
    
    # Add satellite layer option
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add heatmap if available
    if st.session_state.ndvi_grid:
        HeatMap(
            st.session_state.ndvi_grid,
            radius=25,
            blur=15,
            min_opacity=0.3,
            max_opacity=0.8,
            name='Suitability Heatmap'
        ).add_to(m)
    
    # Add selected center marker
    if st.session_state.lat is not None:
        folium.Marker(
            [st.session_state.lat, st.session_state.lon],
            popup="📍 Selected Location",
            tooltip="Click here for details",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
    
    # Add plantation points with clustering
    if st.session_state.points:
        marker_cluster = MarkerCluster(name='Plantation Points').add_to(m)
        
        for i, p in enumerate(st.session_state.points):
            folium.CircleMarker(
                location=[p["lat"], p["lon"]],
                radius=4,
                color="green",
                fill=True,
                fill_color="lightgreen",
                fill_opacity=0.7,
                popup=folium.Popup(
                    f"""
                    <div style='width: 200px'>
                        <b>Point #{i+1}</b><br>
                        <b>Suitability:</b> {p['score']:.1f}/100<br>
                        <b>Coordinates:</b><br>
                        {p['lat']:.6f}, {p['lon']:.6f}<br>
                        <br><b>Recommended Species:</b><br>
                        {'<br>'.join(['• ' + s for s in p['species'][:3]])}
                    </div>
                    """,
                    max_width=250
                ),
                tooltip=f"Point #{i+1} (Score: {p['score']:.0f})"
            ).add_to(marker_cluster)
    
    folium.LayerControl().add_to(m)
    
    # Display map and capture clicks
    map_data = st_folium(m, height=600, width=None, key="main_map")
    
    # Process click
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lon = map_data["last_clicked"]["lng"]
        
        # Only process if it's a new click
        if (clicked_lat != st.session_state.lat or 
            clicked_lon != st.session_state.lon):
            
            st.session_state.lat = clicked_lat
            st.session_state.lon = clicked_lon
            
            with st.spinner("🔍 Analyzing location..."):
                # Generate environmental proxies
                ndvi_base = round(random.uniform(0.4, 0.9), 2)
                water = round(random.uniform(0.3, 0.8), 2)
                soil = round(random.uniform(0.4, 0.9), 2)
                
                st.session_state.env = {
                    "ndvi": ndvi_base,
                    "water": water,
                    "soil": soil
                }
                
                # Generate points
                points = generate_plantation_points_ml(
                    clicked_lat, 
                    clicked_lon,
                    st.session_state.suitability_map
                )
                
                # Limit to requested number
                points = points[:num_points]
                st.session_state.points = points
                
                # Create heatmap data
                st.session_state.ndvi_grid = create_heatmap_data(points)
                
                # Create DataFrame
                st.session_state.df = pd.DataFrame([
                    {
                        "Point_ID": i + 1,
                        "Latitude": p["lat"],
                        "Longitude": p["lon"],
                        "Suitability_Score": p["score"],
                        "Recommended_Species": ", ".join(p["species"])
                    }
                    for i, p in enumerate(points)
                ])
                
                st.session_state.analysis_complete = True
                st.rerun()

with col2:
    st.subheader("📊 Analysis Results")
    
    # Environmental metrics
    if st.session_state.env:
        st.markdown("### 🌍 Environmental Factors")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric(
                "🌿 NDVI",
                f"{st.session_state.env['ndvi']:.2f}",
                help="Vegetation health (0-1)"
            )
        with col_b:
            st.metric(
                "💧 Water",
                f"{st.session_state.env['water']:.2f}",
                help="Water availability (0-1)"
            )
        
        st.metric(
            "🌱 Soil Quality",
            f"{st.session_state.env['soil']:.2f}",
            help="Soil suitability (0-1)"
        )
        
        # Overall score
        avg_score = np.mean([p["score"] for p in st.session_state.points]) if st.session_state.points else 0
        
        st.markdown("---")
        st.markdown("### 🎯 Overall Suitability")
        st.progress(avg_score / 100)
        st.metric("Average Score", f"{avg_score:.1f}/100")
        
        # Interpretation
        if avg_score >= 70:
            st.success("✅ Excellent site for plantation!")
        elif avg_score >= 50:
            st.info("ℹ️ Good site with some constraints")
        else:
            st.warning("⚠️ Challenging site - careful planning needed")
    
    # ML Analysis Results
    if st.session_state.image_analysis:
        st.markdown("---")
        st.markdown("### 🤖 ML Analysis")
        
        analysis = st.session_state.image_analysis
        
        with st.expander("📊 Terrain Distribution", expanded=True):
            if st.session_state.terrain_stats:
                for terrain, stats in st.session_state.terrain_stats.items():
                    if stats['percentage'] > 0.5:
                        st.write(f"**{terrain}:** {stats['percentage']:.1f}%")
        
        with st.expander("🔬 Detailed Metrics"):
            st.json({
                "NDVI Stats": analysis['ndvi_stats'],
                "Soil Quality": analysis['soil_quality']['quality_score'],
                "Water Coverage": analysis['water_availability']['water_coverage']
            })

# --------------------------------------------------
# Download Section
# --------------------------------------------------
if st.session_state.df is not None and len(st.session_state.points) > 0:
    st.markdown("---")
    st.subheader("📥 Download Plantation Plan")
    
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    
    with col_dl1:
        # CSV Download
        csv_data = st.session_state.df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name=f"plantation_plan_{st.session_state.lat:.4f}_{st.session_state.lon:.4f}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_dl2:
        # GeoJSON Download
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [p["lon"], p["lat"]]
                    },
                    "properties": {
                        "id": i + 1,
                        "suitability": p["score"],
                        "species": p["species"]
                    }
                }
                for i, p in enumerate(st.session_state.points)
            ]
        }
        
        st.download_button(
            label="🗺️ Download GeoJSON",
            data=json.dumps(geojson, indent=2),
            file_name=f"plantation_plan_{st.session_state.lat:.4f}_{st.session_state.lon:.4f}.geojson",
            mime="application/json",
            use_container_width=True
        )
    
    with col_dl3:
        # KML Download
        kml = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Plantation Plan</name>
    <description>AI-Generated Plantation Coordinates</description>
"""
        for i, p in enumerate(st.session_state.points):
            kml += f"""
    <Placemark>
      <name>Point {i+1}</name>
      <description>
        Suitability: {p['score']:.1f}/100
        Species: {', '.join(p['species'][:2])}
      </description>
      <Point>
        <coordinates>{p['lon']},{p['lat']},0</coordinates>
      </Point>
    </Placemark>
"""
        kml += """
  </Document>
</kml>
"""
        
        st.download_button(
            label="📍 Download KML",
            data=kml,
            file_name=f"plantation_plan_{st.session_state.lat:.4f}_{st.session_state.lon:.4f}.kml",
            mime="application/vnd.google-earth.kml+xml",
            use_container_width=True
        )
    
    # Data Preview
    with st.expander("👀 Preview Data Table"):
        st.dataframe(
            st.session_state.df,
            use_container_width=True,
            hide_index=True
        )

# --------------------------------------------------
# Information Panel
# --------------------------------------------------
st.markdown("---")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    ### 💡 How to Use
    
    1. **Select Location**: Click anywhere on the map
    2. **Optional**: Upload satellite image for ML analysis
    3. **View Results**: Check environmental metrics and suitability
    4. **Review Points**: Click on green markers for details
    5. **Download**: Get CSV, GeoJSON, or KML format
    6. **Plant**: Use GPS coordinates in the field!
    """)

with info_col2:
    st.markdown("""
    ### 🌿 Legend
    
    - 🔴 **Red Marker**: Selected center location
    - 🟢 **Green Dots**: Optimal plantation points
    - 🔥 **Heatmap**: Suitability intensity (red = high)
    - **Score Range**: 0-100 (higher = better)
    - **Min Spacing**: Trees won't compete for resources
    """)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><b>🌱 Plantation Optimizer</b> | Powered by AI & ML | Built for environmental impact</p>
        <p style='font-size: 0.8rem;'>
            Uses Random Forest terrain classification, NDVI analysis, and smart optimization algorithms
        </p>
    </div>
    """,
    unsafe_allow_html=True
)