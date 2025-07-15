from src.pipeline import analyze_code
from src.logos import LightSpeedLogos

SAMPLE_CODE = """
def analyze_data(data):
    total = 0
    count = 0
    results = []
    
    for value in data:
        total += value
        count += 1
        if value > 100:
            results.append(value)
    
    average = total / count if count > 0 else 0
    return results, average

data = [45, 112, 98, 205]
processed, avg = analyze_data(data)
print(f"Results: {processed}, Average: {avg}")
"""

if __name__ == "__main__":
    # Analyze the sample code
    results = analyze_code(SAMPLE_CODE)
    
    print("=== CODE ANALYSIS RESULTS ===")
    print(f"Original instructions: {results['statistics']['original_length']}")
    print(f"Optimized instructions: {results['statistics']['optimized_length']}")
    print(f"Final symbols: {results['statistics']['logo_length']}")
    print(f"Compression ratio: {results['statistics']['compression_ratio']:.2%}\n")
    
    print("=== LIGHT SPEED LOGOS ===")
    print(" ".join(results['logos']))
    
    print("\n=== ARCHITECTURE FINGERPRINT ===")
    print(results['fingerprint'])
    
    print("\n=== MICRO-OPERATIONS DETECTED ===")
    for name, pattern in results['micro_ops'].items():
        pattern_str = " → ".join([f"{p[0]}({p[1]})" for p in pattern])
        print(f"{name}: {pattern_str}")
