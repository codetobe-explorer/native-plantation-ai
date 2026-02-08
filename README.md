# 🌱 AI-Powered Native Plantation Planning System

An end-to-end AI system that identifies optimal plantation coordinates
and recommends native plant species using geospatial intelligence.

## 🚨 Problem
Large-scale plantation drives often fail due to:
- Poor site selection
- Non-native species
- Lack of data-driven planning

## 💡 Solution
This system uses satellite-derived proxies, environmental modeling,
and ML-based reasoning to generate **100 optimal plantation locations**
for any selected region.

## 🧠 How It Works
1. User selects a location on an interactive map
2. Optional satellite image is analyzed
3. Environmental factors (NDVI, soil, water) are estimated
4. AI generates optimal plantation points
5. Native species are recommended per point
6. Results are exported as CSV / GeoJSON / KML

## 🔬 AI & ML Components
- Terrain classification (ML-ready)
- NDVI-based vegetation analysis
- Suitability scoring & optimization
- Modular ML backend (mocked for hackathon)

## 🛠️ Tech Stack
- Python
- Streamlit
- Folium
- NumPy, Pandas
- OpenCV
- Modular ML architecture

## 🌍 Impact
- Enables NGOs & governments to plan plantations scientifically
- Improves survival rate of planted trees
- Encourages native biodiversity

## 🚀 Deployment
Streamlit Community Cloud

> Note: ML backend uses mock models for hackathon demonstration,
> designed to be replaced with real satellite ML pipelines.
