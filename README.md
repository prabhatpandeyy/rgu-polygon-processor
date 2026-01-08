# RGU Polygon Processor

A user-friendly GUI application to process RGU polygon data and convert it to QGIS-compatible formats.

## Features

- **Easy-to-use GUI**: No need for Jupyter notebooks or command line
- **File picker**: Browse and select input files easily
- **Multiple formats**: Supports CSV, TSV, Excel files (.xlsx, .xls)
- **QGIS-ready output**: Creates GeoPackage (.gpkg) and GeoJSON files
- **Progress tracking**: Real-time processing log and progress bar
- **Windows executable**: Can be distributed as a standalone .exe file

## For End Users (Running the Application)

### Option 1: Use the Executable (Recommended)
1. Download `RGU_Polygon_Processor.exe`
2. Double-click to run (no installation needed)
3. Use the GUI to select your input file and process data

### Option 2: Run from Python
1. Install Python 3.8 or higher
2. Install requirements: `pip install -r requirements.txt`
3. Run: `python rgu_polygon_processor.py`

## For Developers (Building the Executable)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Build Steps
1. Clone or download this repository
2. Open command prompt/terminal in the project folder
3. Run the build script:
   ```bash
   python build_executable.py
   ```
4. The executable will be created in the `dist` folder

### Manual Build (Alternative)
```bash
# Install requirements
pip install -r requirements.txt

# Build executable
pyinstaller --onefile --windowed --name RGU_Polygon_Processor rgu_polygon_processor.py
```

## How to Use

1. **Launch the application**
   - Double-click the .exe file or run the Python script

2. **Select input file**
   - Click "Browse" next to "Input File"
   - Choose your CSV/Excel file containing RGU polygon data

3. **Choose output folder** (optional)
   - Default is "qgis_output" in the same directory
   - Click "Browse" to choose a different location

4. **Process data**
   - Click "Process Data" button
   - Watch the progress in the log area

5. **Use the output**
   - Find the processed files in your output folder
   - Drag and drop .gpkg or .geojson files into QGIS

## Output Files

The application creates several files:

- `rgu_polygons_all.gpkg` - Single GeoPackage with all polygons
- `rgu_polygons_all.geojson` - GeoJSON format (alternative)
- `rgu_polygons_by_date.gpkg` - Separate layers by effective date
- `summary_report.csv` - Summary statistics

## Data Requirements

Your input file should contain:
- A column with polygon data (EWKB hex format)
- Date columns (effective_from_date, effective_to_date)
- Cycle information (CYCLE_1)

The application automatically:
- Filters for year 2025
- Filters for CYCLE_1
- Converts hex polygon data to proper geometries
- Creates QGIS-compatible spatial files

## Troubleshooting

### Common Issues
- **"No data remaining after filters"**: Check if your data has 2025 dates and CYCLE_1 values
- **"Error converting geometry"**: Verify polygon column contains valid EWKB hex data
- **File not found**: Ensure the input file path is correct and accessible

### Getting Help
- Check the processing log for detailed error messages
- Ensure your input file matches the expected format
- Try with a smaller sample file first

## Technical Details

- Built with Python, tkinter (GUI), pandas, and geopandas
- Processes PostGIS EWKB hex geometry data
- Outputs in EPSG:4326 coordinate system
- Supports multi-threading for responsive GUI