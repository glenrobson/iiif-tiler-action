# iiif-tiler-action
A github action to create level0 tiles using [iiif-tiler](https://github.com/glenrobson/iiif-tiler) with a Github action.


## Testing

Unit tests are in the `tests` folder and can be run with:
```
python -m unittest discover -s tests
```

Run single test:
```
python -m unittest tests.test_update_manifest.TestUpdateManifest.test_canvas_label
```
