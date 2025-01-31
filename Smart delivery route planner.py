import matplotlib.pyplot as plt
import math
from itertools import permutations

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def tsp_solver(locations):
    n = len(locations)
    min_distance = float('inf')
    best_route = []

    for perm in permutations(range(1, n)):  # Start from 1 to skip the depot at index 0
        current_route = [0] + list(perm) + [0]  # Include the depot as the start and end
        current_distance = sum(
            calculate_distance(locations[current_route[i]], locations[current_route[i + 1]])
            for i in range(len(current_route) - 1)
        )

        if current_distance < min_distance:
            min_distance = current_distance
            best_route = current_route

    return best_route, min_distance

def optimize_route(locations, priorities):
    priority_map = {'high': 1, 'medium': 2, 'low': 3}
    
    # Separate depot from locations and priorities
    depot_location = locations[0]
    depot_priority = priorities[0]
    locations = locations[1:]
    priorities = priorities[1:]
    
    # Sort locations based on priorities
    sorted_data = sorted(zip(locations, priorities), key=lambda x: priority_map[x[1]])
    sorted_locations = [item[0] for item in sorted_data]

    # Reinsert depot back to the first position
    sorted_locations.insert(0, depot_location)

    # Solve TSP on sorted locations
    best_route, total_distance = tsp_solver(sorted_locations)
    return best_route, total_distance, sorted_locations

def plot_route(locations, best_route, priorities):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Draw the points with colors based on priorities
    colors = {'high': 'red', 'medium': 'blue', 'low': 'green'}
    for i, (location, priority) in enumerate(zip(locations, priorities)):
        # Skip depot handling separately for color
        if priority == 'depot':
            ax.scatter(location[0], location[1], color='gray', label="Depot" if i == 0 else None)
        else:
            ax.scatter(location[0], location[1], color=colors[priority], label=f"{priority} ({location})" if i == 0 else None)
        ax.text(location[0], location[1], str(i), fontsize=12, ha='right')

    # Draw the path
    for i in range(len(best_route) - 1):
        start = locations[best_route[i]]
        end = locations[best_route[i + 1]]
        ax.plot([start[0], end[0]], [start[1], end[1]], color='black', linestyle='--')

    ax.set_title("Optimized Delivery Route")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # Input: Dynamic input from the user
    n = int(input("Enter the number of delivery locations: "))
    locations = []
    priorities = []

    for i in range(n):
        print(f"\nLocation {i + 1}:")
        x = float(input("Enter x-coordinate: "))
        y = float(input("Enter y-coordinate: "))
        priority = input("Enter priority (high/medium/low): ").strip().lower()

        while priority not in ['high', 'medium', 'low']:
            print("Invalid priority. Please enter high, medium, or low.")
            priority = input("Enter priority (high/medium/low): ").strip().lower()

        locations.append((x, y))
        priorities.append(priority)

    # Add depot (starting and ending point)
    locations.insert(0, (0, 0))  
    priorities.insert(0, 'depot')

    # Optimize route
    best_route, total_distance, sorted_locations = optimize_route(locations, priorities)
    print(f"\nOptimized Route: {[sorted_locations[i] for i in best_route]}")
    print(f"Total Distance: {total_distance:.2f} units")

    # Visualize the route
    plot_route(sorted_locations, best_route, priorities)
