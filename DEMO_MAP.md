# Demo Map Feature

## Overview
Added a fake/demo map image that displays whenever a safety score is calculated. This provides visual feedback during demonstrations without requiring actual mapping libraries or API keys.

## Implementation

### Map Generation
Created `generate_fake_map.py` script that generates a static map image showing:
- **Green dot**: Policy location at center
- **Red dots**: 3 SuperFund sites nearby
- **Green circle**: 50-mile radius around policy
- **Grid background**: Simulates map tiles
- **White lines**: Represents roads
- **Legend**: Explains the symbols

**Output**: `data/demo_map.png` (800x600 pixels)

### Display Logic
Updated `render_image_section()` in `app.py` to:
1. Check if `demo_map.png` exists
2. Display the image when score results are available
3. Show location details as caption below the map
4. Fall back to warning if map file not found

### Code Changes

**app.py** - Map rendering section:
```python
if st.session_state.current_score_result:
    # Display fake demo map
    import os
    map_path = os.path.join("data", "demo_map.png")
    if os.path.exists(map_path):
        st.image(map_path, caption="Demo Map - Policy location (green) and nearby SuperFund sites (red)", use_container_width=True)
        
        # Display location info below map
        location = st.session_state.current_score_result['location']
        st.caption(f"📍 Center: {location[0]:.4f}, {location[1]:.4f} | 📏 Radius: {st.session_state.current_score_result['radius_miles']} mi | 🏭 Sites: {st.session_state.current_score_result['site_count']}")
    else:
        st.warning("⚠️ Demo map not found. Run `python generate_fake_map.py` to create it.")
```

## Usage

### Generate Map (One-time)
```bash
python generate_fake_map.py
```

This creates `data/demo_map.png` which will be used for all map displays.

### View in App
1. Run the app: `streamlit run app.py`
2. Execute any address query (e.g., "849 First Street, Portland, ME 04101")
3. Click the **🗺️ Map** button to expand the map section
4. The demo map will appear showing the visualization

## Features

### Current (Demo Mode)
- ✅ Static demo map with symbolic visualization
- ✅ Shows policy location (green) and sites (red)
- ✅ Displays 50-mile radius circle
- ✅ Includes legend for clarity
- ✅ Shows actual coordinates and stats in caption
- ✅ No external dependencies (no API keys needed)
- ✅ Fast rendering (no API calls)

### Future Enhancements
Could be upgraded to show:
- Real map tiles from OpenStreetMap
- Actual policy and site locations
- Interactive markers with site details
- Dynamic zoom levels
- Multiple radius circles
- Color-coded risk zones
- Street names and labels

## Dependencies

### Required
- **Pillow (PIL)**: For image generation
  ```bash
  pip install Pillow
  ```

### Not Required (Benefits of Demo Mode)
- ❌ No Folium
- ❌ No Plotly
- ❌ No Mapbox API key
- ❌ No Google Maps API key
- ❌ No external API calls

## File Structure
```
data/
  demo_map.png          # Generated demo map image
generate_fake_map.py    # Script to create the map
app.py                  # Displays the map in UI
```

## Demo Advantages
1. **Offline**: No internet connection required
2. **Fast**: Instant display, no API latency
3. **Reliable**: No API rate limits or failures
4. **Simple**: No complex mapping library setup
5. **Free**: No API costs
6. **Portable**: Works anywhere, anytime
7. **Professional**: Still looks good for demos

## Notes
- The same map image is shown for all queries (demo purposes only)
- Real coordinates are still shown in the caption
- Map can be upgraded later when ready for production
- Perfect for proof-of-concept demonstrations
