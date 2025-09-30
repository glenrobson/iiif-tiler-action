from iiif_prezi3 import Manifest, config, AnnotationBody, ServiceV2, ServiceV3, Annotation, AnnotationPage, Canvas
import json
import subprocess
import os

config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"
def getUserRepo():
    if "GITHUB_REPOSITORY" in os.environ:
        gitURL=os.environ["GITHUB_REPOSITORY"]
    else:    
        command='git remote -v |grep fetch|grep -o "https://.*.git"'
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
            gitURL=result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error message: {e.stderr}")

    (username, repo) = gitURL.replace("https://github.com/","").split("/")
    repo = repo.replace(".git","")
    return (username,repo)

def createManifest(username, repo, manifestName, imageDir, skipImageValidation=False):    
    manifest = Manifest(id=f"https://{username}.github.io/{repo}/{manifestName}", label=f"All images loaded in {username}/{repo} project")

    info_jsons = {}
    for image in os.listdir(imageDir):
        if os.path.isdir(f"{imageDir}/{image}") and os.path.exists(f"{imageDir}/{image}/info.json"):
            print (f"Adding {imageDir}/{image}/info.json to Manifest")
            with open(f"{imageDir}/{image}/info.json", "r") as file:
                if not skipImageValidation:
                    # Check image is valid before adding
                    if not os.path.isdir(f"{imageDir}/{image}/full"):
                        print (f"Image: {imageDir}/{image} is malformed it doesn't have a full directory.")
                        print ("Skipping")
                        continue
                    

                infoJson = json.load(file)
                root=f"https://{username}.github.io/{repo}/{imageDir}/{image}"

                body = AnnotationBody(id="http://example.com", type="Image")
                if 'type' not in infoJson:
                    # Assume v2

                    # V2 profile contains profile URI plus extra features
                    service = infoJson
                    service["@type"] = "ImageService2"
                    body.service = [service]
                    body.id = f'{infoJson["@id"]}/full/full/0/default.jpg'
                    body.format = "image/jpeg"
                    info_jsons[infoJson["@id"]] = infoJson
                else:
                    service = infoJson
                    body.service = [service]
                    body.id = f'{infoJson["id"]}/full/max/0/default.jpg'
                    body.format = "image/jpeg"
                    info_jsons[infoJson["id"]] = infoJson


                canvas = manifest.make_canvas(id=f"{root}/canvas/", height=infoJson['height'], width=infoJson['width'])
                canvas.add_label(image, language="none")
                annotation = Annotation(id=f"{root}/annotation/", motivation='painting', body=body, target=canvas.id)

                annotationPage = AnnotationPage(id=f"{root}/annotation/AnnoPage")
                annotationPage.add_item(annotation)
                canvas.add_item(annotationPage)

    manifestJson = json.loads(manifest.json())
    # Add full info.jsons
    for canvas in manifestJson["items"]:
        for annoPage in canvas["items"]:
            for anno in annoPage["items"]:
                if "@id" in anno["body"]["service"][0]:
                    anno["body"]["service"][0] = info_jsons[anno["body"]["service"][0]["@id"]]
                else:
                    anno["body"]["service"][0] = info_jsons[anno["body"]["service"][0]["id"]]
    return manifestJson                    

def getEnvironment():
    (username, repo) = getUserRepo()
    manifestName = os.environ["MANIFEST"]
    imageDir = os.environ["IMAGE_DIR"]

    return (username, repo, manifestName, imageDir)

if __name__ == "__main__":
    (username, repo, manifestName, imageDir) = getEnvironment()

    manifest = createManifest(username, repo, manifestName, imageDir)
    print (f"Writing out manifest to {manifestName}")
    #with open(manifestName, "w") as file:
    #    file.write(manifest.jsonld(indent=2))
    # Writing JSON to a file
    with open(manifestName, "w") as json_file:
        json.dump(manifest, json_file, indent=4)