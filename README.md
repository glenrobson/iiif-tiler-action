# iiif-tiler-action
A github action to create level0 tiles using [iiif-tiler](https://github.com/glenrobson/iiif-tiler) with a Github action. The level0 images and manifest.json can be served using Github pages. 

# Usage
This action monitors a directory and if it finds an image it will convert it into a level0 tiled image. It will then go through the output directory and create a manifest.json with links to any images it finds. 

An example directory structure is below:

```
images
  - uploads/2
  - uploads/3
  - manifest.json
```

Inputs:

 * `input-dir-v2` the location to look for images to generate a IIIF version 2 image. Default "images/uploads/2"
 * `input-dir-v3` the location to look for images to generate a IIIF version 3 image. Default "images/uploads/3"
 * `output-dir` the location to store the generated image tiles. Default "images/"
 * `manifest` the location of the manifest which will contain links to all images in the `output-dir`. Default "images/manifest.json"

An example project that uses this action is available at [iiif-test/test2](https://github.com/iiif-test/test2).

## Example action

The following action watches the `images/uploads/` directory and sub directory for uploaded images. It then turns them into level0 IIIF images in the `images` directory and generates a manifest.json in the `images` directory contain links to all of the images. It then commits these images and manifest back to the source repository. 

```
name: convert_images
on: 
  workflow_dispatch:
  push:
    branches:
      - main
    paths:
      - images/uploads/**
permissions:
  contents: write

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  convertimages:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 1
      - uses: glenrobson/iiif-tiler-action@main
        with:
          input-dir-v2: images/uploads/2
          input-dir-v3: images/uploads/3
          output-dir: images
          manifest: images/manifest.json
      - name: commit files
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git config pull.rebase false
          git pull origin main
          git add -A
          git commit -m "Adding IIIF image to repository" -a || echo "No changes to commit"
      - name: push changes
        uses: ad-m/github-push-action@v0.6.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: main 
```          

## Testing

Unit tests are in the `tests` folder and can be run with:
```
python -m unittest discover -s tests
```

Run single test:
```
python -m unittest tests.test_update_manifest.TestUpdateManifest.test_canvas_label
```
