# Backend Overview

The Hyde backend manages simulation jobs and data.  Simulations submited through the front-end are processed through workflows which queue and run the simulations. The backend is connected to the front-end through Redis; the backend program will be listening for run commands from the frontend to start a simulation.

# Backend Dependencies
 * SLURM
 * Fireworks

Fireworks can be installed using the instructions listed in its [documentation](https://materialsproject.github.io/fireworks/installation.html).

# Usage
Starting Hyde requires that MongoDB and controller.py are running on the cluster in question. The user must identify a partition on the cluster which he or she hopes to run a simulation before submitting a job.

