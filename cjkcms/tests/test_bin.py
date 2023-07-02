import os
import shutil
import sys
import unittest
from unittest import mock
from io import StringIO

from cjkcms.bin.cjkcms import main as cms_main
from cjkcms.bin.cjkcms import CreateProject


class TestCjkcmsStart(unittest.TestCase):
    CURR_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEST_DIR = os.path.join(CURR_DIR, "testproject-unittest")

    def setup(self):
        # Clean/create directory to start into
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)
        os.mkdir(self.TEST_DIR)

    def cleanup(self):
        # Cleanup
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)

    def test_help(self):
        # Set args
        sys.argv = ["cjkcms", "help"]

        # Create a StringIO object to capture the console output
        out = StringIO()
        with mock.patch.object(sys, "stdout", new=out):
            # Run
            cms_main()
        self.assertIn("start", out.getvalue())
        self.assertIn(CreateProject.help, out.getvalue())

    def test_help_start(self):
        # Set args
        sys.argv = ["cjkcms", "help", "start"]

        out = StringIO()
        with mock.patch.object(sys, "stdout", new=out):
            # Run
            cms_main()
        self.assertIn("name", out.getvalue())
        self.assertIn("[directory]", out.getvalue())

    def test_default(self):
        self.setup()
        # Set args
        sys.argv = ["cjkcms", "start", "myproject", self.TEST_DIR]
        # prevent output
        out = StringIO()
        with mock.patch.object(sys, "stdout", new=out):
            # Run
            cms_main()
        # Assert files exist
        self.assertTrue(os.path.exists(os.path.join(self.TEST_DIR, "README.md")))
        self.cleanup()

    def test_allopts(self):
        self.setup()
        # Set args
        sys.argv = [
            "cjkcms",
            "start",
            "myproject",
            self.TEST_DIR,
            "--template",
            "basic",
            "--sitename",
            "CjkCorp, Inc.",
            "--domain",
            "example.com",
        ]
        # prevent output
        out = StringIO()
        with mock.patch.object(sys, "stdout", new=out):
            # Run
            cms_main()
        # Assert files exist
        self.assertTrue(os.path.exists(os.path.join(self.TEST_DIR, "README.md")))
        self.cleanup()

    def test_domain_www(self):
        self.setup()
        # Set args
        sys.argv = [
            "cjkcms",
            "start",
            "superproject",
            self.TEST_DIR,
            "--domain",
            "www.superproject.com",
        ]
        # prevent output
        out = StringIO()
        with mock.patch.object(sys, "stdout", new=out):
            # Run
            cms_main()

        # Assert files exist
        self.assertTrue(os.path.exists(os.path.join(self.TEST_DIR, "README.md")))
        self.cleanup()

    def test_template_sass(self):
        self.setup()
        # Set args
        sys.argv = [
            "cjkcms",
            "start",
            "webpack_project",
            self.TEST_DIR,
            "--template",
            "webpack",
        ]
        # prevent output
        out = StringIO()
        with mock.patch.object(sys, "stdout", new=out):
            # Run
            cms_main()

        # Assert files exist
        self.assertTrue(os.path.exists(os.path.join(self.TEST_DIR, "README.md")))
        self.cleanup()
