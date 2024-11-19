import subprocess
import os
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
    output = os.environ["OUTPUT"]
    for filename in os.listdir(input_dir):
        (id, extension) =os.path.splitext(filename)
        if extension not in (".md"):
            if not os.path.exists(f"{output}/{id}"):
                try:
                    print(f'Converting {filename} to {output}/{id}')        
                    command = generateCommand(f"{input_dir}/{filename}")
                    result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
                    print (result.stdout)
                except subprocess.CalledProcessError as e:
                    print(f"Command failed with return code {e.returncode}")
                    print(f"Error message: {e.stderr}")
            else:
                print(f'Image {filename} already exists in {output}/{id}')        
        else:
            print (f"Skipping {filename}")        

if __name__ == "__main__":
    convertImages()