import csv
from io import StringIO
from collections import defaultdict, OrderedDict
import statistics

class OLAPCube:
    def __init__(self, data_string):
        """Initialize OLAP cube with wine dataset"""
        self.data = self.parse_data(data_string)
        self.dimensions = ['quality', 'alcohol_range', 'pH_range', 'density_range']
        self.measures = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar']
        
    def parse_data(self, data_string):
        """Parse the semicolon-separated data"""
        lines = data_string.strip().split('\n')
        headers = [col.strip('"') for col in lines[0].split(';')]
        
        data = []
        for line in lines[1:]:
            if line.strip():
                values = line.split(';')
                row = {}
                for i, header in enumerate(headers):
                    try:
                        row[header] = float(values[i])
                    except ValueError:
                        row[header] = values[i]
                
                # Create dimension categories
                row['alcohol_range'] = self.categorize_alcohol(row['alcohol'])
                row['pH_range'] = self.categorize_pH(row['pH'])
                row['density_range'] = self.categorize_density(row['density'])
                row['quality'] = int(row['quality'])
                
                data.append(row)
        
        return data
    
    def categorize_alcohol(self, alcohol):
        """Categorize alcohol content"""
        if alcohol < 9.5:
            return 'Low (< 9.5)'
        elif alcohol < 11.5:
            return 'Medium (9.5-11.5)'
        else:
            return 'High (> 11.5)'
    
    def categorize_pH(self, pH):
        """Categorize pH levels"""
        if pH < 3.2:
            return 'Very Acidic (< 3.2)'
        elif pH < 3.4:
            return 'Acidic (3.2-3.4)'
        else:
            return 'Less Acidic (> 3.4)'
    
    def categorize_density(self, density):
        """Categorize density"""
        if density < 0.996:
            return 'Light (< 0.996)'
        elif density < 0.998:
            return 'Medium (0.996-0.998)'
        else:
            return 'Heavy (> 0.998)'
    
    def print_table(self, title, headers, rows):
        """Print data in tabular format"""
        print(f"\n{'='*60}")
        print(f"{title}")
        print('='*60)
        
        # Calculate column widths
        col_widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Print headers
        header_line = "| " + " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths)) + " |"
        print(header_line)
        print("|" + "-" * (len(header_line) - 2) + "|")
        
        # Print rows
        for row in rows:
            row_line = "| " + " | ".join(f"{str(cell):<{w}}" for cell, w in zip(row, col_widths)) + " |"
            print(row_line)
        
        print()
    
    def rollup(self, dimension_hierarchy, measure='fixed acidity', agg_func='avg'):
        """
        Rollup operation - aggregate data from detailed to summary level
        dimension_hierarchy: list of dimensions from detailed to summary
        """
        print(f"ROLLUP OPERATION on '{measure}' using {agg_func}")
        
        for level, dim in enumerate(dimension_hierarchy):
            print(f"\nLevel {level + 1}: Aggregating by {dim}")
            
            # Group data by current dimension
            groups = defaultdict(list)
            for record in self.data:
                groups[record[dim]].append(record[measure])
            
            # Calculate aggregation
            headers = [dim.title(), f'{measure.title()} ({agg_func.upper()})', 'Count']
            rows = []
            
            for key, values in sorted(groups.items()):
                if agg_func == 'avg':
                    agg_value = round(statistics.mean(values), 2)
                elif agg_func == 'sum':
                    agg_value = round(sum(values), 2)
                elif agg_func == 'max':
                    agg_value = round(max(values), 2)
                elif agg_func == 'min':
                    agg_value = round(min(values), 2)
                
                rows.append([key, agg_value, len(values)])
            
            self.print_table(f"Rollup Level {level + 1}: {dim}", headers, rows)
    
    def drilldown(self, start_dimension, drill_dimensions, measure='fixed acidity', agg_func='avg'):
        """
        Drilldown operation - break down summary data into detailed levels
        """
        print(f"DRILLDOWN OPERATION on '{measure}' using {agg_func}")
        
        all_dims = [start_dimension] + drill_dimensions
        
        for level in range(1, len(all_dims) + 1):
            current_dims = all_dims[:level]
            print(f"\nLevel {level}: Drilling down by {' + '.join(current_dims)}")
            
            # Group data by current dimensions combination
            groups = defaultdict(list)
            for record in self.data:
                key = tuple(record[dim] for dim in current_dims)
                groups[key].append(record[measure])
            
            # Calculate aggregation
            headers = [dim.title() for dim in current_dims] + [f'{measure.title()} ({agg_func.upper()})', 'Count']
            rows = []
            
            for key, values in sorted(groups.items()):
                if agg_func == 'avg':
                    agg_value = round(statistics.mean(values), 2)
                elif agg_func == 'sum':
                    agg_value = round(sum(values), 2)
                elif agg_func == 'max':
                    agg_value = round(max(values), 2)
                elif agg_func == 'min':
                    agg_value = round(min(values), 2)
                
                if isinstance(key, tuple):
                    row = list(key) + [agg_value, len(values)]
                else:
                    row = [key, agg_value, len(values)]
                rows.append(row)
            
            self.print_table(f"Drilldown Level {level}: {' + '.join(current_dims)}", headers, rows)
    
    def slice_operation(self, dimension, value, measures=None):
        """
        Slice operation - select a subset of the cube by fixing one dimension
        """
        if measures is None:
            measures = ['fixed acidity', 'volatile acidity', 'alcohol']
        
        print(f"SLICE OPERATION: {dimension} = {value}")
        
        # Filter data for the specific dimension value
        filtered_data = [record for record in self.data if record[dimension] == value]
        
        if not filtered_data:
            print(f"No data found for {dimension} = {value}")
            return
        
        # Calculate statistics for each measure
        headers = ['Measure', 'Count', 'Average', 'Min', 'Max', 'Sum']
        rows = []
        
        for measure in measures:
            values = [record[measure] for record in filtered_data]
            rows.append([
                measure,
                len(values),
                round(statistics.mean(values), 2),
                round(min(values), 2),
                round(max(values), 2),
                round(sum(values), 2)
            ])
        
        self.print_table(f"Slice: {dimension} = {value}", headers, rows)
        
        # Show sample records
        print(f"\nSample records (first 5):")
        sample_headers = ['Quality', 'Alcohol', 'pH', 'Fixed Acidity', 'Volatile Acidity']
        sample_rows = []
        for i, record in enumerate(filtered_data[:5]):
            sample_rows.append([
                record['quality'],
                record['alcohol'],
                record['pH'],
                record['fixed acidity'],
                record['volatile acidity']
            ])
        
        self.print_table("Sample Records", sample_headers, sample_rows)
    
    def dice_operation(self, conditions, measures=None):
        """
        Dice operation - select a subset by applying conditions on multiple dimensions
        conditions: dict of {dimension: value/range}
        """
        if measures is None:
            measures = ['fixed acidity', 'volatile acidity', 'alcohol']
        
        print(f"DICE OPERATION with conditions: {conditions}")
        
        # Filter data based on all conditions
        filtered_data = []
        for record in self.data:
            match = True
            for dim, condition in conditions.items():
                if isinstance(condition, (list, tuple)) and len(condition) == 2:
                    # Range condition
                    if not (condition[0] <= record[dim] <= condition[1]):
                        match = False
                        break
                else:
                    # Exact match condition
                    if record[dim] != condition:
                        match = False
                        break
            
            if match:
                filtered_data.append(record)
        
        if not filtered_data:
            print("No data found matching the conditions")
            return
        
        print(f"Found {len(filtered_data)} records matching conditions")
        
        # Calculate statistics for each measure
        headers = ['Measure', 'Count', 'Average', 'Min', 'Max', 'Sum']
        rows = []
        
        for measure in measures:
            values = [record[measure] for record in filtered_data]
            rows.append([
                measure,
                len(values),
                round(statistics.mean(values), 2),
                round(min(values), 2),
                round(max(values), 2),
                round(sum(values), 2)
            ])
        
        self.print_table("Dice Results", headers, rows)
        
        # Show distribution by quality
        quality_dist = defaultdict(int)
        for record in filtered_data:
            quality_dist[record['quality']] += 1
        
        dist_headers = ['Quality', 'Count', 'Percentage']
        dist_rows = []
        total = len(filtered_data)
        for quality in sorted(quality_dist.keys()):
            count = quality_dist[quality]
            percentage = round((count / total) * 100, 1)
            dist_rows.append([quality, count, f"{percentage}%"])
        
        self.print_table("Quality Distribution", dist_headers, dist_rows)

# Function to read CSV file
def read_csv_file(filename):
    """Read CSV file and return as string"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        print("Make sure the file is in the same directory as this script.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Read data from CSV file
csv_filename = "winequality-red.csv"  # Change this to your CSV filename
csv_data = read_csv_file(csv_filename)


# Create OLAP cube instance
print(f"Loading data from: {csv_filename}")
cube = OLAPCube(csv_data)
print(f"Successfully loaded {len(cube.data)} records")

print("WINE DATASET OLAP OPERATIONS DEMO")
print("="*60)

# 1. ROLLUP Operation
cube.rollup(['alcohol_range', 'pH_range', 'quality'], measure='fixed acidity', agg_func='avg')

# 2. DRILLDOWN Operation  
cube.drilldown('quality', ['alcohol_range', 'pH_range'], measure='volatile acidity', agg_func='avg')

# 3. SLICE Operation
cube.slice_operation('quality', 5, measures=['fixed acidity', 'volatile acidity', 'alcohol'])

# 4. DICE Operation
cube.dice_operation({
    'quality': [6, 8],  # Quality between 6 and 8
    'alcohol_range': 'Medium (9.5-11.5)'  # Medium alcohol range
}, measures=['fixed acidity', 'volatile acidity', 'citric acid'])

print("\n" + "="*60)
print("OLAP OPERATIONS COMPLETED")
print("="*60)

# Instructions for customizing operations:
print("""
CUSTOMIZATION OPTIONS:

1. Change CSV filename:
   - Modify 'csv_filename' variable at the top

2. Customize categorization ranges in class methods:
   - categorize_alcohol() - for alcohol content ranges
   - categorize_pH() - for pH level ranges  
   - categorize_density() - for density ranges

3. Available OLAP operations:
   - rollup(dimension_hierarchy, measure, agg_func)
   - drilldown(start_dimension, drill_dimensions, measure, agg_func)
   - slice_operation(dimension, value, measures)
   - dice_operation(conditions, measures)

4. Supported aggregation functions: 'avg', 'sum', 'max', 'min'

5. Available dimensions: 'quality', 'alcohol_range', 'pH_range', 'density_range'

6. Available measures: All numeric columns from your dataset

EXAMPLE USAGE:
- cube.rollup(['quality'], measure='alcohol', agg_func='avg')
- cube.slice_operation('quality', 7)
- cube.dice_operation({'quality': [6, 8], 'alcohol_range': 'High (> 11.5)'})
""")
