# Cellular Automata Simulation App

This project is visualisation tool for cellular automata, focused primarily around Conway's Game of Life, however, additional rules for celluar automata are available to experiment with.

![Gif](CellularAutomataVideo.gif)

## Setup

This project is managed with [poetry](https://python-poetry.org/), which can be installed on Linux/Mac/WSL by:
```shell
curl -sSL https://install.python-poetry.org | python3 -
```

The application's packages can then be installed by running:
```shell
poetry install
```
inside of the base directory

## Usage

The application can then be run by:
```shell
poetry run python3 main.py
```

## Controls & Tools

The application provides UI panels to the left of the simulation space with various control buttons.

### First Panel - Simulation Controls
The first panel contains tools to control the running of the simulation.
The slider affects the framerate of the simulation, allowing you to speed it up or slow it down.
The simulation can be paused/played pressing the pause/play button, or pressing the **\<space\>** key.\
The simulation can be interated over whilst paused, using the next button, or pressing the **\<enter\>** key.

### Second Panel - Seeds and Grid Clearing
The second panel contains the tools to randomly populate the grid, either using a new random seed, or entering
a pre-determined one. This allows you to run random simulations and watch the interactions between many cells.
Pressing the "Use seed" button will populate the grid using the currently entered seed.
The grid can also be cleared from this panel to reset the simulation space. 

### Third Panel - Rules and States
The third panel allows you to control the Cellular Automata Rule, and save/load grid states. The Cellular Automata Rule defaults to "Game of Life", 
which follows the rules of Conway's Game of Life, "Rule 30", "Rule 90", "Rule 110" and "Rule 184". Switching between these rules will slightly alter the behaviour
of the cells and therefore the result of the simulation. Combine this tool with a set seed to view the differences in the simulations. The "Load Rule State" button loads a grid we have defined for that rule state. In the case of "Game of Life", this grid is populated with some interesting oscillators and other shapes which behave interestingly with this rule.
The "Save Grid State" and "Load Grid State" buttons open file dialogs to allow your to save or load the simulation space. If a simulation state loaded with this button was created with a seed, that seed can be found by pressing the "Current Seed" button to view that seed.

### Fouth Panel - Brush Controls
The fourth panel defines the controls for different brush types and sizes. The circle tool is set by default, and the width of this circle tool can be adjusted with the brush size slider.
The dropwdown allows the tool type to be changed from the circle, to one of the defined stamp shapes. These stamp shapes are common automatons within Conway's Game of Life, allowing you to easily add and combine these within the simulation grid.
In order to use any of these special brushes, you must press the "Paint" button to toggle them on. With the paint button toggled, you can click and hold to draw on the simulation space.
Clicking the "Erase" button will similarly allow you to click and hold, but to kill alive cells. The brush size also affects the eraser tool.

Without any brush controls selected, cells on the grid can have their states toggled by clicking on the cell with the primary mouse button. It is best to pause the application
before editing any cells, as cells placed on their own will die immediately with the simulation still running.


## Testing

You can run the tests for this application by:
```shell
poetry run pytest
```
