# 🌱 AI-Powered Native Plantation Planning System

![Version](https://img.shields.io/badge/version-2.0.0-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

An intelligent plantation planning system that uses machine learning and satellite imagery analysis to optimize tree planting locations. The system integrates custom ML models with Tambo.ai's satellite intelligence API to provide data-driven recommendations for native species plantation.

---

## 🎯 Features

### Core Capabilities
- **Interactive Map Interface**: Click-to-select location with real-time visualization
- **Dual AI Backend**:
  - 🤖 Custom ML: Local terrain & vegetation analysis using Random Forest classifiers
  - 🚀 Tambo.ai: Cloud-based satellite intelligence API integration
- **Smart Point Generation**: AI-optimized placement of 50-200 plantation points
- **Species Recommendations**: Native species suggestions based on environmental factors
- **Multiple Export Formats**: CSV, GeoJSON, and KML downloads

### Analysis Features
- **NDVI (Normalized Difference Vegetation Index)** calculation
- **Terrain classification** (forest, agricultural, urban, water, barren)
- **Soil quality assessment**
- **Water availability mapping**
- **Suitability scoring** (0-100 scale)
- **Environmental factor analysis**

### Visualization
- **Interactive heatmaps** showing plantation suitability
- **Marker clustering** for better map performance
- **Satellite/street view** layer switching
- **Real-time metrics** and confidence scores

---

## 📋 Prerequisites

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- Internet connection for map tiles and Tambo.ai API

### Required Python Packages
```bash
streamlit>=1.28.0
streamlit-folium>=0.15.0
folium>=0.14.0
pandas>=2.0.0
numpy>=1.24.0
Pillow>=10.0.0
requests>=2.31.0
scikit-learn>=1.3.0
```

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/codetobe-explorer/plantation-optimizer.git
cd plantation-optimizer
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Project Structure
Ensure your project structure looks like this:
```
plantation-optimizer/
├── app/
│   └── app.py                 # Main Streamlit application
├── src/
│   ├── recommendation/
│   │   └── species.py         # Species recommendation logic
│   ├── optimization/
│   │   ├── grid.py           # Grid generation
│   │   └── suitability.py    # Suitability scoring
├── utils/
│   └── image_analyzer.py      # Custom ML image analysis
├── models/
│   └── terrain_classifier.py # Terrain classification model
├── requirements.txt
└── README.md
```

### 5. Configure Tambo.ai API (Optional)
```bash
# Set environment variable
export TAMBOAI_API_KEY="your_api_key_here"

# Or create a .env file
echo "TAMBOAI_API_KEY=your_api_key_here" > .env
```

---

## 💻 Usage

### Starting the Application
```bash
streamlit run app/app.py
```

The application will open in your default browser at `http://localhost:8501`

### Basic Workflow

#### 1. **Select a Location**
   - Click anywhere on the interactive map
   - The system will set this as your plantation center point

#### 2. **Upload Satellite Image (Optional)**
   - Click "Upload Satellite Image" in the sidebar
   - Supported formats: PNG, JPG, JPEG
   - Recommended: High-resolution satellite imagery

#### 3. **Choose Analysis Method**
   
   **Option A: Custom ML Analysis**
   - Click "🔍 Analyze with ML"
   - Uses local Random Forest terrain classifier
   - Analyzes NDVI, soil, and water availability
   - No API key required
   
   **Option B: Tambo.ai Analysis**
   - Enable Tambo.ai in sidebar settings
   - Click "🚀 Analyze with Tambo.ai"
   - Cloud-based satellite intelligence
   - Requires API key
   - Higher confidence scores

#### 4. **Configure Settings**
   - **Number of Points**: 50-200 (default: 100)
   - **Minimum Spacing**: 2-10 meters (default: 3m)
   - Adjust based on tree species and site conditions

#### 5. **Review Results**
   - View environmental metrics (NDVI, water, soil)
   - Check overall suitability score
   - Click individual green markers for species recommendations
   - Review terrain distribution statistics

#### 6. **Download Plantation Plan**
   - **CSV**: Spreadsheet format with all data
   - **GeoJSON**: For GIS applications
   - **KML**: For Google Earth/Maps

---

## 📊 Understanding the Output

### Suitability Score (0-100)
- **70-100**: Excellent site - highly recommended
- **50-69**: Good site - suitable with minor considerations
- **30-49**: Moderate site - may require site preparation
- **0-29**: Challenging site - significant constraints

### Environmental Factors
- **NDVI (0-1)**: Vegetation health indicator
  - 0.6-1.0: Dense, healthy vegetation
  - 0.3-0.6: Moderate vegetation
  - 0.0-0.3: Sparse/stressed vegetation
  
- **Water Availability (0-1)**: Moisture and water access
  - 0.7-1.0: High water availability
  - 0.4-0.7: Moderate water access
  - 0.0-0.4: Low water availability
  
- **Soil Quality (0-1)**: Soil suitability
  - 0.7-1.0: Excellent soil conditions
  - 0.4-0.7: Good soil with amendments
  - 0.0-0.4: Poor soil - requires improvement

### Terrain Classifications
- **Forest**: Dense tree coverage
- **Agricultural**: Croplands and farmland
- **Urban**: Built-up areas
- **Water**: Rivers, lakes, ponds
- **Barren**: Exposed soil/rock

---

## 🔧 Configuration

### Customizing Point Generation
Edit parameters in `app.py`:
```python
# Minimum pixel spacing between trees
min_pixel_spacing = 15  # Increase for wider spacing

# Suitability threshold
suitable_mask = suitability_map > 50  # Adjust threshold

# Number of points
num_points = st.slider("Number of plantation points", 50, 200, 100, 10)
```

### Adding Custom Species
Edit `src/recommendation/species.py`:
```python
def recommend_species(ndvi, water, soil):
    species_list = []
    
    # Add your custom logic
    if ndvi > 0.7 and water > 0.6:
        species_list.append("Your Custom Species")
    
    return species_list
```

### Modifying Suitability Algorithm
Edit `src/optimization/suitability.py`:
```python
def compute_suitability(ndvi, water, soil):
    # Customize weights
    score = (ndvi * 0.4) + (water * 0.3) + (soil * 0.3)
    return score * 100
```

---

## 🌐 API Integration

### Tambo.ai API Usage
The system sends requests to Tambo.ai with the following structure:

```python
payload = {
    "image": base64_encoded_image,
    "coordinates": {
        "latitude": lat,
        "longitude": lon
    },
    "analysis_type": "plantation_suitability",
    "parameters": {
        "return_suitability_map": True,
        "return_species_recommendations": True,
        "return_environmental_factors": True
    }
}
```

**Response Format:**
```json
{
    "suitability_scores": [[0.8, 0.7, ...], ...],
    "recommended_species": ["Oak", "Pine", "Maple"],
    "environmental_factors": {
        "ndvi": 0.75,
        "water_availability": 0.65,
        "soil_quality": 0.80
    },
    "confidence_score": 0.92
}
```

---

## 📁 Output File Formats

### 1. CSV Format
```csv
Point_ID,Latitude,Longitude,Suitability_Score,Recommended_Species
1,23.0226,72.5715,85.3,"Oak, Pine, Teak"
2,23.0227,72.5716,82.1,"Neem, Banyan, Peepal"
```

### 2. GeoJSON Format
```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [72.5715, 23.0226]
            },
            "properties": {
                "id": 1,
                "suitability": 85.3,
                "species": ["Oak", "Pine", "Teak"]
            }
        }
    ]
}
```

### 3. KML Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <Placemark>
            <name>Point 1</name>
            <description>Suitability: 85.3/100</description>
            <Point>
                <coordinates>72.5715,23.0226,0</coordinates>
            </Point>
        </Placemark>
    </Document>
</kml>
```

---

## 🛠️ Troubleshooting

### Common Issues

**1. Map Not Loading**
```bash
# Check internet connection
# Clear browser cache
# Try different browser
```

**2. ML Analysis Fails**
```bash
# Ensure all ML dependencies installed
pip install scikit-learn numpy pillow

# Check image format (PNG/JPG only)
```

**3. Tambo.ai API Errors**
```bash
# Verify API key is set
echo $TAMBOAI_API_KEY

# Check API quota/limits
# Ensure image size < 10MB
```

**4. No Points Generated**
```bash
# Lower suitability threshold in code
# Check if location selected on map
# Verify environmental data available
```

**5. Memory Issues**
```bash
# Reduce number of points
# Use smaller satellite images
# Increase system RAM
```

---

## 🔒 Security & Privacy

- **API Keys**: Never commit API keys to version control
- **Environment Variables**: Use `.env` files (add to `.gitignore`)
- **Data Privacy**: Uploaded images are processed locally or via secure API
- **No Data Storage**: Session data cleared on browser close

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions
- Include unit tests for new features
- Update README for major changes

---

## 📝 Changelog

### Version 2.0.0 (Current)
- ✅ Tambo.ai API integration
- ✅ Dual AI backend support
- ✅ Enhanced terrain classification
- ✅ Improved UI/UX
- ✅ Multiple export formats

### Version 1.0.0
- ✅ Basic map interface
- ✅ Custom ML analysis
- ✅ Species recommendation
- ✅ CSV export

---

## 📚 References

- **Streamlit Documentation**: https://docs.streamlit.io
- **Folium Documentation**: https://python-visualization.github.io/folium/
- **Tambo.ai API**: https://api.tambo.ai/docs
- **NDVI Calculation**: https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index
- **Random Forest**: https://scikit-learn.org/stable/modules/ensemble.html#forest

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- Harsh Bhati

## 🙏 Acknowledgments

- Tambo.ai for satellite intelligence API
- Streamlit team for the amazing framework
- OpenStreetMap contributors for map data
- Esri for satellite imagery tiles
- Environmental science community for research

---

## 📧 Support

For questions and support:
- **Email**: harshbhatimultiverse@gmail.com
---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

---

**Made with 💚 for a greener planet**
