"""
Run NumCalc on one or multiple Mesh2HRTF project folders.

This script monitors the RAM and CPU usage and starts a new NumCalc instance
whenever enough resources are available. A log file is written to the base
directory and an error is raised if any unfinished instances are detected.

HOW TO USE
----------
run ``python num_calc_manager -h`` for help (requires Python and psutil).

Tips:
  1- It is not recommended to run multiple NumCalcManager.py scripts on the
     same computer (but it would work)
  2- avoid folder names with spaces. Code is not tested for that.
  3- If there is a problem with some instance result delete its output folder
     folder "be.X" and the Manager will automatically re-run that instance on
     the next run.
"""

import os
import psutil
import argparse
import mesh2hrtf as m2h

# parse command line input ----------------------------------------------------
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--project_path", default=False, type=str,
    help=("The working directory. This can be a directory that contains "
          "multiple Mesh2HRTF project folders, a Mesh2HRTF project folder or "
          "a NumCalc folder inside a Mesh2HRTF project folder. The default "
          "uses the directory containing this file"))
parser.add_argument(
    "--numcalc_path", default=False, type=str,
    help=("On Unix, this is the path to the NumCalc binary (by default "
          "'NumCalc' is used). On Windows, this is the path to the folder "
          "'NumCalc_WindowsExe' from "
          "https://sourceforge.net/projects/mesh2hrtf-tools/ (by default "
          "the project_path is searched for this folder)"))
parser.add_argument(
    "--max_ram_load", default=False, type=float,
    help=("The RAM that can maximally be used in GB. New NumCalc instances are"
          " only started if enough RAM is available. By default all available "
          "RAM will be used."))
parser.add_argument(
    "--ram_safety_factor", default=1.05, type=float,
    help=("A safety factor that is applied to the estimated RAM consumption. "
          "The estimate is obtained using NumCalc -estimate_ram. The default "
          "of 1.05 would for example assume that 10.5 GB ram are needed if "
          "a RAM consumption of 10 GB was estimated by NumCalc."))
parser.add_argument(
    "--max_cpu_load", default=90, type=int,
    help=("Maximum allowed CPU load in percent. New instances are only "
          "launched if the current CPU load is below this value. The default "
          "is 90 percent."))
parser.add_argument(
    "--max_instances", default=0, type=int,
    help=("The maximum numbers of parallel NumCalc instances. By default a new"
          " instance is launched until the number of available CPU cores given"
          " by ``psutil.cpu_count()`` is reached."))
parser.add_argument(
    "--wait_time", default=15, type=int,
    help=("Delay in seconds for waiting until the RAM and CPU usage is checked"
          " in case too little resources are available for starting the next. "
          "NumCalc instance."))
parser.add_argument(
    "--starting_order", default='alternate',
    choices=('alternate', 'high', 'low'), type=str,
    help=("Control the order in which the frequency steps are launched. "
          "'high' always launches the step with the highest possible "
          "memory consumption. 'low', launches the step with the lowest "
          "estimated memory consumption, and the default 'alternate' mixes "
          "the two approaches."))
parser.add_argument(
    "--confirm_errors", default='True', choices=('True', 'False'), type=str,
    help=("If True, num_calc_manager waits for user input in case an error "
          "occurs."))

args = vars(parser.parse_args())

# default values --------------------------------------------------------------
args["project_path"] = args["project_path"] if args["project_path"] \
    else os.path.dirname(os.path.realpath(__file__))

if os.name == "nt":
    args["numcalc_path"] = args["numcalc_path"] if args["numcalc_path"] \
        else None
else:
    args["numcalc_path"] = args["numcalc_path"] if args["numcalc_path"] \
        else None

args["max_ram_load"] = None if args["max_ram_load"] is False \
     else args["max_ram_load"]

args["max_instances"] = psutil.cpu_count() if args["max_instances"] == 0 \
    else args["max_instances"]

# launch numcalc_manager ------------------------------------------------------
m2h.numcalc_manager(
    args["project_path"],
    args["numcalc_path"],
    args["max_ram_load"],
    args["ram_safety_factor"],
    args["max_cpu_load"],
    args["max_instances"],
    args["wait_time"],
    args["starting_order"],
    args["confirm_errors"] == 'True')