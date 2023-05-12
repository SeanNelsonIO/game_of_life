# Cellular Automata Simulation App

This project is visualisation tool for cellular automata, focused primarily around Conway's Game of Life, however, additional rules for celluar automata are available to experiment with.

This project is developed by:
**Sean Nelson** *(ll17s2n)* and **Steven Taylor** *(sc18sst)*

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

### Controls

The application provides UI panels to the left of the simulation space with various control buttons.\
The simulation can be paused/played pressing the pause/play button, or pressing the **\<space\>** key.\
The simulation can be interated over whilst paused, using the next button, or pressing the **\<n\>** key.


Cells on the grid can have their states toggled by clicking on the cell with the primary mouse button. It is best to pause the application
before editing any cells, as cells placed on their own will die immediately with the simulation still running.\
There are additional tools to edit the cell grid, 


## Testing

You can run the tests for this application by:
```shell
poetry run pytest
```

## Documentation

Aside from the user manual 
All of the code files in this submission have been documented using numpy style docstrings.

## Statement of Contribution

For this group project, we divided the task among the group of 3 into the code implementation, by Steven Taylor and Sean Nelson,
as well as a critical exploration of Conway's Game of Life, written solely by Farnaaz Gahazaani.

Breakdown for the code implementation:
The project began initially with Sean building out the Cellular Automata logic, found in *cellular_automata.py* and *rules.py*,
And Steven built out the graphical application to visualise, control and manipulate the the simulations, this code is found primarily between
the files *cellular_automata_app.py* and *cell_grid.py* and implements Sean's code for the underlying cellular automata code.

Beyond the early version of the implementation, work became much more intertwined and we each made contributions to eachother's separate pieces of work
in order to build a better overall application, with both contributing additional features to both the visual application and improving on the Cellular Automata logic.
Sean primarily worked on extending the drawing tools available to the user, and Steven extending the tools to allow for saving and loading simulations which allows for
interesting 

Each file in the code submission contains a primary author tag which denotes who produced the majority of the work for each file. However both contributors have
each made improvements and changes to all of the files within the project. We have made the github repository public in order for these direct contributions to be visible
to the markers. We feel that directly separating these pieces of work would not have been beneficial to the overall quality of the project and have utilised our
different strengths to produce a project which we are proud of and happy to present. Both of us working on the code project feel that we have equally produced good
quality work that has culminated in both an even distribution of tasks and 