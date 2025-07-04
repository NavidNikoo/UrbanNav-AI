# UrbanNav-Ai 🚗🧠  
**AI Pathfinding Simulator for Self-Driving Cars**

UrbanNav-Ai is an AI visualization tool built with Python and Pygame that simulates how autonomous vehicles navigate grid-based environments using advanced search algorithms. It compares A*, Uniform Cost Search, and Iterative Deepening on 2D maps with real-time visual feedback, traffic rules, and adaptive heuristics.

---

## 🔧 Key Features

- Visualizes:
  - A* Search (with Manhattan & Euclidean heuristics)
  - Uniform Cost Search (UCS)
  - Iterative Deepening (IDS)
- "Learn" mode: adapt A* heuristic based on feedback from optimal paths
- Interactive 2D grid environment:
  - Set start/goal positions
  - Add walls (obstacles)
  - Add stop signs 🚫 and traffic lights 🚦 with weighted traversal costs
- Real-time stats: execution time, memory usage, explored nodes
- PNG-based UI for clean macOS compatibility
- Designed with autonomous car routing logic in mind

---

## 🎯 Project Goal

To bring search algorithms to life — not just in theory, but in practical, visual, and interactive ways that mimic the decision-making of self-driving vehicles navigating city traffic.

---

## 🧱 Project Structure

```plaintext
main.py               # Main loop, UI buttons, grid event handling
algorithm.py          # A*, UCS, IDS implementations with stats
heuristic_update.py   # Learning mode: updates A* heuristics over time
visualization.py      # Rendering grid states, weights, and icons
assets/               # PNG icons for stop signs, traffic, etc.

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
git clone https://github.com/NavidNikoo/UrbanNav-Ai.git
cd UrbanNav-Ai
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
- Click Reset → clear grid
- Right-click a node to reset it


## License
- This project is licensed under the GNU General Public License v3.0

Screenshots
Demo
![image](https://github.com/user-attachments/assets/c1a3869f-5f19-4616-a03b-d3556807e2d3)
![image](https://github.com/user-attachments/assets/cde9ca21-010d-45d7-ac48-a44d43c8700f)
![image](https://github.com/user-attachments/assets/f5a1d0c5-54fd-44ee-aad2-19c8b24c6852)
















##Resources



