# David Alonso Bayona Timana
# ID: 8968801
#
# Universidad Pontificia Javeriana De Cali

import random
import sys
import matplotlib.pyplot as plt
import numpy as np

def fcfs(iniPos, requests):
    movements = []
    positions = [iniPos]
    total_movement = 0
    current = iniPos
    
    for request in requests:
        movement = abs(current - request)
        total_movement += movement
        current = request
        movements.append(movement)
        positions.append(current)
    
    return total_movement, positions, movements

def scan(iniPos, requests):
    req_list = requests.copy()
    total_movement = 0
    current = iniPos
    positions = [iniPos]
    movements = []
    
    # Separate requests
    above = sorted([r for r in req_list if r >= current])
    below = sorted([r for r in req_list if r < current], reverse=True)
    
    # Upward sweep
    for request in above:
        movement = abs(current - request)
        total_movement += movement
        current = request
        movements.append(movement)
        positions.append(current)
    
    # Downward sweep if needed
    if below:
        movement_to_end = abs(current - 4999)
        total_movement += movement_to_end
        current = 4999
        movements.append(movement_to_end)
        positions.append(current)
        
        for request in below:
            movement = abs(current - request)
            total_movement += movement
            current = request
            movements.append(movement)
            positions.append(current)
    
    return total_movement, positions, movements

def c_scan(iniPos, requests):
    req_list = requests.copy()
    total_movement = 0
    current = iniPos
    positions = [iniPos]
    movements = []
    
    # Separate requests
    above = sorted([r for r in req_list if r >= current])
    below = sorted([r for r in req_list if r < current])
    
    # Upward sweep
    for request in above:
        movement = abs(current - request)
        total_movement += movement
        current = request
        movements.append(movement)
        positions.append(current)
    
    # Jump to start and continue upward
    if below:
        movement_to_end = abs(current - 4999)
        jump_to_start = 4999 - 0
        total_movement += movement_to_end + jump_to_start
        current = 0
        movements.append(movement_to_end)
        positions.append(4999)  # Show the jump point
        movements.append(jump_to_start)
        positions.append(0)
        
        for request in below:
            movement = abs(current - request)
            total_movement += movement
            current = request
            movements.append(movement)
            positions.append(current)
    
    return total_movement, positions, movements

def create_visualization(initial_pos, requests, fcfs_data, scan_data, cscan_data):

    # Extract data
    fcfs_total, fcfs_positions, fcfs_movements = fcfs_data
    scan_total, scan_positions, scan_movements = scan_data
    cscan_total, cscan_positions, cscan_movements = cscan_data
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Head Movement Paths
    plt.subplot(2, 2, 1)
    plt.plot(range(len(fcfs_positions)), fcfs_positions, 'b-', label='FCFS', alpha=0.7, linewidth=1)
    plt.plot(range(len(scan_positions)), scan_positions, 'r-', label='SCAN', alpha=0.7, linewidth=1)
    plt.plot(range(len(cscan_positions)), cscan_positions, 'g-', label='C-SCAN', alpha=0.7, linewidth=1)
    plt.axhline(y=initial_pos, color='k', linestyle='--', alpha=0.5, label='Start Position')
    plt.xlabel('Request Sequence')
    plt.ylabel('Cylinder Position')
    plt.title('Disk Head Movement Paths')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Performance Comparison Bar Chart
    plt.subplot(2, 2, 2)
    algorithms = ['FCFS', 'SCAN', 'C-SCAN']
    movements = [fcfs_total, scan_total, cscan_total]
    colors = ['lightblue', 'lightcoral', 'lightgreen']
    
    bars = plt.bar(algorithms, movements, color=colors, edgecolor='black', alpha=0.7)
    plt.ylabel('Total Head Movement (cylinders)')
    plt.title('Total Head Movement Comparison')
    
    # Add value labels on bars
    for bar, value in zip(bars, movements):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000, 
                f'{value:,}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Movement per Request (first 50 requests for clarity)
    plt.subplot(2, 2, 3)
    n_show = min(50, len(fcfs_movements))
    x = range(1, n_show + 1)
    
    plt.plot(x, fcfs_movements[:n_show], 'bo-', label='FCFS', markersize=3, alpha=0.7)
    plt.plot(x, scan_movements[:n_show], 'rs-', label='SCAN', markersize=3, alpha=0.7)
    plt.plot(x, cscan_movements[:n_show], 'g^-', label='C-SCAN', markersize=3, alpha=0.7)
    
    plt.xlabel('Request Number')
    plt.ylabel('Head Movement per Request (cylinders)')
    plt.title('Movement per Request (First 50 Requests)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 4. Efficiency Metrics
    plt.subplot(2, 2, 4)
    metrics = ['Total Movement', 'Avg Movement/Req', 'Efficiency vs FCFS']
    fcfs_metrics = [fcfs_total, fcfs_total/len(requests), 0]
    scan_metrics = [scan_total, scan_total/len(requests), ((fcfs_total-scan_total)/fcfs_total)*100]
    cscan_metrics = [cscan_total, cscan_total/len(requests), ((fcfs_total-cscan_total)/fcfs_total)*100]
    
    x_pos = np.arange(len(metrics))
    width = 0.25
    
    plt.bar(x_pos - width, fcfs_metrics, width, label='FCFS', color='lightblue', edgecolor='black')
    plt.bar(x_pos, scan_metrics, width, label='SCAN', color='lightcoral', edgecolor='black')
    plt.bar(x_pos + width, cscan_metrics, width, label='C-SCAN', color='lightgreen', edgecolor='black')
    
    plt.xlabel('Performance Metrics')
    plt.ylabel('Values')
    plt.title('Algorithm Efficiency Comparison')
    plt.xticks(x_pos, metrics)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    
    # Adjust layout and display
    plt.tight_layout()
    plt.show()
    
    # Print detailed performance analysis
    print("\n" + "="*60)
    print("DETAILED PERFORMANCE ANALYSIS")
    print("="*60)
    print(f"{'Metric':<25} {'FCFS':<12} {'SCAN':<12} {'C-SCAN':<12}")
    print("-"*60)
    print(f"{'Total Movement':<25} {fcfs_total:<12,} {scan_total:<12,} {cscan_total:<12,}")
    print(f"{'Avg Movement/Request':<25} {fcfs_total/len(requests):<12.1f} {scan_total/len(requests):<12.1f} {cscan_total/len(requests):<12.1f}")
    print(f"{'Efficiency vs FCFS':<25} {'0%':<12} {((fcfs_total-scan_total)/fcfs_total)*100:<11.1f}% {((fcfs_total-cscan_total)/fcfs_total)*100:<11.1f}%")
    print(f"{'Requests Serviced':<25} {len(requests):<12} {len(requests):<12} {len(requests):<12}")
    
    # System Responsiveness Analysis
    print("\nSYSTEM RESPONSIVENESS ANALYSIS:")
    print(f"- FCFS: Simple and fair, but poor performance for random workloads")
    print(f"- SCAN: Good balance of performance and fairness, no starvation")
    print(f"- C-SCAN: More uniform wait times, better for time-sensitive applications")

def main():
    # Command line arguments
    if len(sys.argv) != 2:
        print("Usage: python diskScheduling.py <initial_position>")
        sys.exit(1)
    try:
        initial_position = int(sys.argv[1])
        if initial_position < 0 or initial_position > 4999:
            print("Error: Initial position must be between 0 and 4999")
            sys.exit(1)
    except ValueError:
        print("Error: Initial position must be an integer")
        sys.exit(1)
    
    # Generate 1000 random cylinder requests
    random.seed(42)  # For reproducible results
    requests = [random.randint(0, 4999) for _ in range(1000)]
    
    # Calculate results for all algorithms
    print("Calculating disk scheduling algorithms...")
    fcfs_data = fcfs(initial_position, requests)
    scan_data = scan(initial_position, requests)
    cscan_data = c_scan(initial_position, requests)
    
    # Basic results
    print("\nBASIC RESULTS:")
    print(f"FCFS  Total movement: {fcfs_data[0]:,} cylinders")
    print(f"SCAN  Total movement: {scan_data[0]:,} cylinders") 
    print(f"C-SCAN Total movement: {cscan_data[0]:,} cylinders")
    
    # Create visualization
    create_visualization(initial_position, requests, fcfs_data, scan_data, cscan_data)


main()