# examples/complex_program.py
"""
A complex program demonstrating multiple computational patterns:
- Data processing pipeline
- Mathematical computations
- Class-based OOP
- File I/O operations
- Error handling
- Decorators
"""

import json
import math
from datetime import datetime
from pathlib import Path

# Decorator for timing functions
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        duration = datetime.now() - start
        print(f"{func.__name__} executed in {duration.total_seconds():.4f} seconds")
        return result
    return wrapper

# Data processing class
class DataAnalyzer:
    def __init__(self, data):
        self.data = data
        self.stats = {
            'mean': 0,
            'std_dev': 0,
            'min': float('inf'),
            'max': float('-inf')
        }
    
    def calculate_stats(self):
        """Calculate basic statistics"""
        if not self.data:
            return
        
        # Calculate mean
        total = 0
        count = 0
        for value in self.data:
            total += value
            count += 1
            if value < self.stats['min']:
                self.stats['min'] = value
            if value > self.stats['max']:
                self.stats['max'] = value
        
        self.stats['mean'] = total / count
        
        # Calculate standard deviation
        variance = 0
        for value in self.data:
            variance += (value - self.stats['mean']) ** 2
        self.stats['std_dev'] = math.sqrt(variance / count)
    
    def filter_outliers(self, threshold=2):
        """Filter data points beyond threshold standard deviations"""
        filtered = []
        for value in self.data:
            if abs(value - self.stats['mean']) <= threshold * self.stats['std_dev']:
                filtered.append(value)
        return filtered
    
    @timing_decorator
    def process_data(self):
        """Full data processing pipeline"""
        self.calculate_stats()
        filtered = self.filter_outliers()
        return {
            'original_count': len(self.data),
            'filtered_count': len(filtered),
            'stats': self.stats,
            'filtered_data': filtered
        }

# Mathematical computations
def fibonacci(n):
    """Generate Fibonacci sequence"""
    a, b = 0, 1
    fib_sequence = []
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

def prime_factors(n):
    """Compute prime factors of a number"""
    factors = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

# File operations
@timing_decorator
def process_data_file(file_path):
    """Process data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        analyzer = DataAnalyzer(data['values'])
        result = analyzer.process_data()
        
        # Create output directory if needed
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        # Save results
        output_path = output_dir / 'analysis_results.json'
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Results saved to {output_path}")
        return result
    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}")
    except KeyError:
        print("Error: Missing 'values' key in JSON data")

# Main execution
if __name__ == "__main__":
    # Generate sample data
    sample_data = [10, 20, 30, 40, 100, 150, 200, 1000]
    
    # Demonstrate DataAnalyzer
    print("=== Data Analysis ===")
    analyzer = DataAnalyzer(sample_data)
    analysis_result = analyzer.process_data()
    print(f"Mean: {analysis_result['stats']['mean']:.2f}")
    print(f"Filtered count: {analysis_result['filtered_count']}")
    
    # Demonstrate mathematical functions
    print("\n=== Mathematical Computations ===")
    n = 20
    fib = fibonacci(n)
    print(f"First {n} Fibonacci numbers: {fib}")
    
    num = 123456
    factors = prime_factors(num)
    print(f"Prime factors of {num}: {factors}")
    
    # Demonstrate file processing
    print("\n=== File Processing ===")
    # Create sample data file
    data_file = Path('data.json')
    with open(data_file, 'w') as f:
        json.dump({
            "source": "generated_data",
            "values": [15, 25, 35, 45, 150, 250, 350, 1500]
        }, f)
    
    # Process the file
    file_result = process_data_file(data_file)
    
    # Clean up temporary files
    data_file.unlink(missing_ok=True)
    output_file = Path('output/analysis_results.json')
    output_file.unlink(missing_ok=True)
    output_file.parent.rmdir()
