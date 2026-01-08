import pandas as pd
import geopandas as gpd
from shapely import wkb
from shapely.geometry import shape
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import sys

class RGUPolygonProcessor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RGU Polygon Processor")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_folder = tk.StringVar(value="qgis_output")
        self.processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="RGU Polygon Data Processor", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file selection
        ttk.Label(main_frame, text="Input File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_file, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_input_file).grid(row=1, column=2, pady=5)
        
        # Output folder selection
        ttk.Label(main_frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_folder, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_output_folder).grid(row=2, column=2, pady=5)
        
        # Process button
        self.process_btn = ttk.Button(main_frame, text="Process Data", command=self.start_processing)
        self.process_btn.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to process data")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Log text area
        log_frame = ttk.LabelFrame(main_frame, text="Processing Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Instructions
        instructions = """Instructions:
1. Click 'Browse' next to 'Input File' to select your CSV/Excel file
2. Optionally change the output folder (default: 'qgis_output')
3. Click 'Process Data' to convert your data to QGIS-compatible formats
4. The processed files will be saved in the output folder

Supported file formats: CSV, TSV, Excel (.xlsx, .xls)
Output formats: GeoPackage (.gpkg), GeoJSON (.geojson)"""
        
        self.log_text.insert(tk.END, instructions)
        self.log_text.config(state=tk.DISABLED)
        
    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("All Supported", "*.csv;*.tsv;*.xlsx;*.xls"),
                ("CSV files", "*.csv"),
                ("TSV files", "*.tsv"),
                ("Excel files", "*.xlsx;*.xls"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)
            
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
            
    def log_message(self, message):
        """Add message to log text area"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"\n{message}")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
        
    def start_processing(self):
        """Start processing in a separate thread"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file")
            return
            
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "Input file does not exist")
            return
            
        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Processing...")
        
        # Clear log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Start processing in separate thread
        thread = threading.Thread(target=self.process_data)
        thread.daemon = True
        thread.start()
        
    def process_data(self):
        """Process the data (runs in separate thread)"""
        try:
            result = self.process_rgu_data(self.input_file.get(), self.output_folder.get())
            
            self.root.after(0, self.processing_complete, True, "Processing completed successfully!")
            
        except Exception as e:
            error_msg = f"Error during processing: {str(e)}"
            self.root.after(0, self.processing_complete, False, error_msg)
            
    def processing_complete(self, success, message):
        """Called when processing is complete"""
        self.processing = False
        self.process_btn.config(state=tk.NORMAL)
        self.progress.stop()
        
        if success:
            self.status_label.config(text="Processing completed successfully!")
            messagebox.showinfo("Success", message)
        else:
            self.status_label.config(text="Processing failed")
            messagebox.showerror("Error", message)

    def hex_to_geometry(self, hex_string):
        """Convert EWKB hex string to Shapely geometry"""
        try:
            if pd.isna(hex_string) or hex_string == '' or hex_string is None:
                return None
            hex_string = str(hex_string).strip()
            geom = wkb.loads(bytes.fromhex(hex_string))
            return geom
        except Exception as e:
            self.log_message(f"Error converting geometry: {e}")
            return None

    def process_rgu_data(self, input_file, output_folder="qgis_output"):
        """Process RGU polygon data and create QGIS-compatible files"""
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # STEP 1: Read the file
        self.log_message("Step 1: Reading file...")
        
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file, sep=None, engine='python')
        elif input_file.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(input_file)
        elif input_file.endswith('.tsv'):
            df = pd.read_csv(input_file, sep='\t')
        else:
            try:
                df = pd.read_csv(input_file, sep='\t')
            except:
                df = pd.read_csv(input_file)

        self.log_message(f"   Total rows loaded: {len(df)}")
        self.log_message(f"   Columns found: {list(df.columns)}")

        # STEP 2: Apply Filters
        self.log_message("\nStep 2: Applying filters...")
        
        # Find columns
        year_col = None
        for col in df.columns:
            if 'effective_from' in col.lower() or col.lower() == 'effective_from_date':
                year_col = col
                break

        cycle_col = None
        for col in df.columns:
            if 'cycle' in col.lower():
                cycle_col = col
                break

        effective_to_col = None
        for col in df.columns:
            if 'effective_to' in col.lower():
                effective_to_col = col
                break

        polygon_col = None
        for col in df.columns:
            if 'rgu_attainment_intersection_polygon' in col.lower() or 'polygon' in col.lower():
                polygon_col = col
                break

        self.log_message(f"   Year column identified: {year_col}")
        self.log_message(f"   Cycle column identified: {cycle_col}")
        self.log_message(f"   Effective_to column identified: {effective_to_col}")
        self.log_message(f"   Polygon column identified: {polygon_col}")

        # Convert date columns
        if year_col:
            df[year_col] = pd.to_datetime(df[year_col], errors='coerce')
        if effective_to_col:
            df[effective_to_col] = pd.to_datetime(df[effective_to_col], errors='coerce')

        # Apply filters
        if year_col:
            df_filtered = df[df[year_col].dt.year == 2025].copy()
            self.log_message(f"   After year 2025 filter: {len(df_filtered)} rows")
        else:
            df_filtered = df.copy()
            self.log_message("   Warning: Year column not found, skipping year filter")

        if cycle_col:
            df_filtered = df_filtered[df_filtered[cycle_col] == 'CYCLE_1'].copy()
            self.log_message(f"   After CYCLE_1 filter: {len(df_filtered)} rows")
        else:
            self.log_message("   Warning: Cycle column not found, skipping cycle filter")

        if len(df_filtered) == 0:
            raise Exception("No data remaining after filters!")

        # STEP 3: Process Polygons
        self.log_message("\nStep 3: Processing polygons...")
        
        df_filtered['geometry'] = df_filtered[polygon_col].apply(self.hex_to_geometry)
        df_filtered = df_filtered[df_filtered['geometry'].notna()].copy()
        self.log_message(f"   Valid geometries: {len(df_filtered)}")

        unique_dates = df_filtered[effective_to_col].dropna().unique()
        self.log_message(f"   Unique effective_to_dates: {len(unique_dates)}")

        # STEP 4: Create QGIS Output Files
        self.log_message("\nStep 4: Creating QGIS output files...")
        
        # Single GeoPackage with all data
        self.log_message("\n   Creating single GeoPackage with all data...")
        gdf_all = gpd.GeoDataFrame(
            df_filtered[[effective_to_col, 'geometry']].copy(),
            geometry='geometry',
            crs='EPSG:4326'
        )
        gdf_all.rename(columns={effective_to_col: 'effective_to_date'}, inplace=True)
        gdf_all['effective_to_date'] = gdf_all['effective_to_date'].astype(str)
        
        gpkg_path = os.path.join(output_folder, 'rgu_polygons_all.gpkg')
        gdf_all.to_file(gpkg_path, driver='GPKG')
        self.log_message(f"   Saved: {gpkg_path}")

        # GeoJSON file
        self.log_message("\n   Creating GeoJSON file...")
        geojson_path = os.path.join(output_folder, 'rgu_polygons_all.geojson')
        gdf_all.to_file(geojson_path, driver='GeoJSON')
        self.log_message(f"   Saved: {geojson_path}")

        # Separate layers for each date
        self.log_message("\n   Creating separate layers for each effective_to_date...")
        gpkg_layers_path = os.path.join(output_folder, 'rgu_polygons_by_date.gpkg')
        
        for i, date in enumerate(sorted(unique_dates)):
            if pd.isna(date):
                continue
            date_str = str(date)[:10] if not pd.isna(date) else 'no_date'
            layer_name = f"date_{date_str.replace('-', '_')}"
            gdf_date = gdf_all[gdf_all['effective_to_date'].str[:10] == date_str].copy()
            
            if len(gdf_date) > 0:
                if i == 0:
                    gdf_date.to_file(gpkg_layers_path, layer=layer_name, driver='GPKG')
                else:
                    gdf_date.to_file(gpkg_layers_path, layer=layer_name, driver='GPKG', mode='a')
                self.log_message(f"      Layer '{layer_name}': {len(gdf_date)} features")
        
        self.log_message(f"   Saved: {gpkg_layers_path}")

        # STEP 5: Create Summary Report
        self.log_message("\nStep 5: Creating summary report...")
        summary = df_filtered.groupby(effective_to_col).size().reset_index(name='polygon_count')
        summary_path = os.path.join(output_folder, 'summary_report.csv')
        summary.to_csv(summary_path, index=False)
        self.log_message(f"   Saved: {summary_path}")

        # Final Summary
        self.log_message("\n" + "="*60)
        self.log_message("PROCESSING COMPLETE!")
        self.log_message("="*60)
        self.log_message(f"\nOutput files created in '{output_folder}' folder:")
        self.log_message(f"  1. rgu_polygons_all.gpkg       - Single file with all polygons")
        self.log_message(f"  2. rgu_polygons_all.geojson    - GeoJSON alternative")
        self.log_message(f"  3. rgu_polygons_by_date.gpkg   - Separate layers by date")
        self.log_message(f"  4. summary_report.csv          - Summary of polygons per date")
        self.log_message(f"\nTotal polygons processed: {len(df_filtered)}")
        self.log_message(f"Unique effective_to_dates: {len(unique_dates)}")
        self.log_message("\nTo use in QGIS:")
        self.log_message("  - Simply drag and drop any .gpkg or .geojson file into QGIS")
        self.log_message("  - The 'effective_to_date' column will be available for labeling")

        return gdf_all

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RGUPolygonProcessor()
    app.run()