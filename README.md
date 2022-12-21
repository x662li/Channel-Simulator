# Channel-Simulator
Channel Assignment (Static / Dynamic) simulator

### Introduction
In this project, we will investigate the optimal power level to maximize the performance of GSM channel assignment in both static and dynamic modes.

The analysis will be done using a simulator developed using Python.

The simulator is consist of the following parts:

- Map: the map with 64 (8x8) cell objects.
- Cell: the container for users. For static case, each cell has a set of available frequencies (90 frequencies) assigned using minimum reuse distance.
- User: individual MNs, resides in a cell and has an assigned frequency.
- Utils: the utility class, contains simulator interfaces (functions).

The simulation is discretized into iterations. For each run, we will first generate some users at the beginning, then for each iteration, we will randomly choose an operation among "generate user", "handover" and "remove user".

For user generation, we randomly pick a cell, create a new user, assign a frequency and add to the cell. In static case, availble frequencies of cell is checked, and in dynamic cases, minimum reuse distance is checked. Failed cases will be recorded as "blocked"

For handover, we randomly pick an existing user and a neighbouring cell of that user, then we move the user to the new cell and assign a new frequency. The checking procedure is the same as user generation. Failed cases will be recoreded as "dropped".

For user removal, we randomly pick an existing user and remove it from the cell. The frequency it used is freed from the cell (static) or the coordinate (dynamic)

### Experiment Metrics

- blocking rate: # blocks / total # operations
- dropping rate: # drops / total # operations
- frequency reuse rate: # frequency reuses (all freqs) / total # operations
- The total number of operations counts for user generations and handovers only.

### Recomended Parameters

- Initial user: 2000
- Iteration: 50000
- Power level: from 2 to 8
- Minimum reuse distace: power level * 1
- Map size: 8x8
