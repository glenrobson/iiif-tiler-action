import subprocess
import os
import os, sys
sys.path.append(os.path.dirname(__file__))
from . import updateManifest

def getUserRepo():
    return updateManifest.getUserRepo()

def generateCommand(filename):
    version = os.environ["IIIF_VERSION"]
    output = os.environ["OUTPUT"]
    (username, project) = getUserRepo()

    return f'java -jar iiif-tiler.jar -identifier "https://{username}.github.io/{project}/{output}/" -version "{version}" -output {output}/ {filename}'

def convertImages():
    input_dir = os.environ["INPUT_DIR"]
    for filename in os.listdir(input_dir):
        try:
            command = generateCommand(f"{input_dir}/{filename}")
            result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
            print (result)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error message: {e.stderr}")

if __name__ == "__main__":
    convertImages()