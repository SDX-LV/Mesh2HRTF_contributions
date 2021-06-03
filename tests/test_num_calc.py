import subprocess
import tempfile
import shutil
import os

# create a temporary directory
tmp = tempfile.TemporaryDirectory(dir=os.getcwd())


def test_build():
    """ test if make for NumCalc works """

    shutil.copytree("../mesh2hrtf/NumCalc/Source", tmp.name+"/NumCalc")
    tmp_path = os.path.join(tmp.name, "NumCalc")
    subprocess.run(["make"], cwd=tmp_path, check=True)