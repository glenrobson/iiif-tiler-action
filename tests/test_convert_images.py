import unittest
import os

from iiif_level0_action import convertImages

class TestConvertImages(unittest.TestCase):

    def test_command(self):
        os.environ["IIIF_VERSION"] = "2"
        os.environ["OUTPUT"] = "tests/images"
        os.environ["GITHUB_REPOSITORY"] = "https://github.com/test/test-repo.git"

        cmd = 'java -jar iiif-tiler.jar -identifier "https://test.github.io/test-repo/tests/images/" -version "2" -output tests/images/ image.jpg'
        self.assertEqual(convertImages.generateCommand("image.jpg"), cmd)