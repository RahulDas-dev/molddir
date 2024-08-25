import os
import shutil
import tempfile
import unittest

from molddir.walker import FolderWalker


class TestFolderWalker(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        # Create some files and directories
        os.makedirs(os.path.join(self.test_dir, "dir1"))
        os.makedirs(os.path.join(self.test_dir, "dir2"))
        with open(os.path.join(self.test_dir, ".gitignore"), "a") as f:
            f.write("dir2\n")  # Add dir2 to the ignore list
        with open(os.path.join(self.test_dir, "file1.txt"), "w") as f:
            f.write("content")
        with open(os.path.join(self.test_dir, "dir1", "file2.txt"), "w") as f:
            f.write("content")
        with open(os.path.join(self.test_dir, ".gitignore"), "w") as f:
            f.write("*.log\n")
            f.write("dir2\n")

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_initialization_valid_path(self):
        fw = FolderWalker(self.test_dir)
        self.assertEqual(fw._codebase_path, self.test_dir)

    def test_initialization_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            FolderWalker("/invalid/path")

    def test_initialization_with_custom_escape(self):
        fw = FolderWalker(self.test_dir, escape="custom_dir,*.tmp")
        self.assertIn("custom_dir", fw._ignore_list)
        self.assertIn("*.tmp", fw._ignore_list)

    def test_populate_gitignore(self):
        fw = FolderWalker(self.test_dir)
        self.assertIn("*.log", fw._ignore_list)

    def test_populate_paths(self):
        fw = FolderWalker(self.test_dir)
        self.assertIn(os.path.join(self.test_dir, "file1.txt"), fw._current_paths)
        self.assertIn(os.path.join(self.test_dir, "dir1", "file2.txt"), fw._current_paths)

    def test_should_ignore(self):
        fw = FolderWalker(self.test_dir)
        self.assertTrue(fw._should_ignore(os.path.join(self.test_dir, "dir2")))
        self.assertFalse(fw._should_ignore(os.path.join(self.test_dir, "file1.txt")))

    def test_match_pattern(self):
        fw = FolderWalker(self.test_dir)
        self.assertTrue(fw._match_pattern("dir2", "dir2"))
        self.assertTrue(fw._match_pattern("dir2/file.log", "*.log"))
        self.assertFalse(fw._match_pattern("dir2/file.txt", "*.log"))

    def test_iteration(self):
        fw = FolderWalker(self.test_dir)
        paths = list(fw)
        self.assertIn(os.path.join(self.test_dir, "file1.txt"), paths)
        self.assertIn(os.path.join(self.test_dir, "dir1", "file2.txt"), paths)


if __name__ == "__main__":
    unittest.main()
