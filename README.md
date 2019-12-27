# Eight Puzzle Problem

> The 8-puzzle consists of an area divided into a grid, 3 by 3 for the 8-puzzle. On each grid square is a tile, expect for one square which remains empty. Thus, there are eight tiles in the 8-puzzle . A tile that is next to the empty grid square can be moved into the empty space, leaving its previous position empty in turn. Tiles are numbered, 1 through 8 for the 8-puzzle, so that each tile can be uniquely identified.
The aim of the puzzle is to achieve a given configuration of tiles from a given (different) configuration by sliding the individual tiles around the grid as described above.[1](http://www.aiai.ed.ac.uk/~gwickler/eightpuzzle-uninf.html)

In this repo I'll be finding solution for 8 Puzzle Problem using A* algorithm using Manhattan distance. To build the state space tree I'll be using [pydot](https://github.com/pydot/pydot) which is a Python wrapper  for [graphviz](https://www.graphviz.org/download/).

## Requirements
```
pydot==1.4.1
```
Graphviz Binary
Download graphviz https://www.graphviz.org/download/

## Usage

 - Download [graphviz binary](https://www.graphviz.org/download/) 
 - Open solve.py and  update  the directory to point graphviz bin directory
```
# Set it to bin folder of graphviz
os.environ["PATH"] += os.pathsep +  'C:/Program Files (x86)/Graphviz2.38/bin/'
``` 
- Install all the requirements
```
pip install -r requirements.txt
``` 
```
python main.py
``` 

The state space tree is saved as "out.png".
## Screenshots
![enter image description here](https://github.com/sarangbishal/8-Puzzle-Problem/blob/master/assets/out.png)