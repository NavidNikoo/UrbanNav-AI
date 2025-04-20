#Search Algorithm Visualizer
- An AI program that demonstrates how self can find best path using different pathfinding algorithms 

## Team Members
- Biplove GC
- Navid Nikoo
- MinJae Kim
- Adam Kaci

##  Key Features
- Set start and end points on a grid
- Draw walls to create obstacles.
- Selecting different algorithm to compare the results
- Give visual feedback for explored nodes
- Real time feedback on heuristic cost
- Displays results such as time consumption, explored, and memory usuage
- Update heuristics for A* algorithm

## Porject Structure
 - main.py : Manages the user interface and event handling for running and comparing pathfinding algorithms with interactive grid control.
 - algorithm.py : Implements core search algorithms (A*, UCS, Iterative Deepening) and visualization of explored paths, execution stats, and memory usage.
 - heuristic_update.py : Contains logic for initializing and updating heuristic values based on Euclidean distance and feedback from previous pathfinding runs.
 - visualization.py : Handles the visual rendering of the grid, node states, heuristic values, and traffic modifiers using Pygame.
 - README.md

## Prequisites

Using Python version 3.12.6
- Python: Install Python 3.10 or later.
- Virtual Environment: Setup virtual environment
- pip: Ensure you have `pip` installed to manage Python packages.
- Pygame: Install Pygame

## Setup Instructions
1. Clone the Repository
```bash
git clone https://github.com/NavidNikoo/A-Search-Manhattan.git
cd A-Search-Manhattan
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate   # For Windows
```
3. Install Dependencies
```bash
pip3 install pygame
```
4. Run the Server
```
python3 main.py
```
## Controls:
- Click on Start → click a node to set the start point
- Click on Goal → click a node to set the goal point
- Click on Block → click nodes to create barriers (walls)
- Click on Stop Sign or Traffic → place traffic modifiers
- Click Run A*, Run UCS, or Run ID to start an algorithm
- Click Learn → run feedback-based heuristic updates
- Click Stats → view execution time, explored nodes, and memory usage
- Right-click a node to reset it

## License
-This project is licensed under the GNU General Public License v3.0

Screenshots
Demo
![image](https://github.com/user-attachments/assets/c1a3869f-5f19-4616-a03b-d3556807e2d3)
![image](https://github.com/user-attachments/assets/cde9ca21-010d-45d7-ac48-a44d43c8700f)
![image](https://github.com/user-attachments/assets/f5a1d0c5-54fd-44ee-aad2-19c8b24c6852)
















##Resources



