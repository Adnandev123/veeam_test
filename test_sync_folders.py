import shutil
import os
import tempfile
import unittest
import argparse
import os
import time
import argparse
import logging
import filecmp
import shutil


from sync_folders import SyncFolders


class TestSyncFolders(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.TemporaryDirectory()
        # Define the src and dst paths
        self.src = self.test_dir.name + "\\src"
        self.dst = self.test_dir.name + "\\dst"
        # Create the src and dst directories
        os.makedirs(self.src)
        os.makedirs(self.dst)
        # Create a SyncFolders object for testing
        self.syncer = SyncFolders(self.src, self.dst, 5, "log_test.txt")
        # Create a file in the dst folder
        open(os.path.join(self.dst, "test.txt"), "w").close()

    def tearDown(self):
        # Delete the temporary directory after the test case is done
        self.test_dir.cleanup()

    def test_same_folders(self):
        # Run the sync_folders function
        self.syncer.sync_folders(self.src, self.dst)
        # Verify that the function did not make any changes to the folders
        self.assertEqual(filecmp.dircmp(self.src, self.dst).left_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).right_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_dirs, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_files, [])

    def test_src_empty(self):
        # Create a file in the dst folder
        open(os.path.join(self.dst, "test.txt"), "w").close()
        # Run the sync_folders function
        self.syncer.sync_folders(self.src, self.dst)
        # Verify that the file was removed from the dst folder
        self.assertEqual(filecmp.dircmp(self.src, self.dst).left_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).right_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_dirs, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_files, [])

    def test_src_has_new_file(self):
        # Create a file in the src folder
        open(os.path.join(self.src, "test.txt"), "w").close()
        # Run the sync_folders function
        self.syncer.sync_folders(self.src, self.dst)
        # Verify that the file was copied to the dst folder
        self.assertEqual(filecmp.dircmp(self.src, self.dst).left_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).right_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_dirs, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_files, ["test.txt"])

    def test_src_modified_file(self):
        # Create a file in both the src and dst folders
        src_file = open(os.path.join(self.src, "test.txt"), "w")
        src_file.write("test")
        src_file.close()
        shutil.copy(src_file.name, self.dst)
        # Modify the file in the src folder
        src_file = open(src_file.name, "w")
        src_file.write("modified")
        src_file.close()
        # Run the sync_folders function
        self.syncer.sync_folders(self.src, self.dst)
        # Verify that the modified file was copied to the dst folder
        self.assertEqual(filecmp.dircmp(self.src, self.dst).left_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).right_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_dirs, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_files, ["test.txt"])
        dst_file = open(os.path.join(self.dst, "test.txt"), "r")
        self.assertEqual(dst_file.read(), "modified")
        dst_file.close()

    def test_src_has_new_folder(self):
        # Create a folder in the src folder
        os.mkdir(os.path.join(self.src, "test"))
        # Run the sync_folders function
        self.syncer.sync_folders(self.src, self.dst)
        # Verify that the folder was copied to the dst folder
        self.assertEqual(filecmp.dircmp(self.src, self.dst).left_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).right_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_dirs, ["test"])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_files, [])

    def test_dst_has_extra_file(self):
        # Create a file in both the src and dst folders
        src_file = open(os.path.join(self.src, "test.txt"), "w")
        src_file.close()
        shutil.copy(src_file.name, self.dst)
        # Create an extra file in the dst folder
        open(os.path.join(self.dst, "extra.txt"), "w").close()
        # Run the sync_folders function
        self.syncer.sync_folders(self.src, self.dst)
        # Verify that the extra file was removed from the dst folder
        self.assertEqual(filecmp.dircmp(self.src, self.dst).left_only, [])
        self.assertEqual

    def test_dst_has_extra_folder(self):
        # Create a folder in both the src and dst folders
        os.mkdir(os.path.join(self.src, "test"))
        shutil.copytree(os.path.join(self.src, "test"), os.path.join(self.dst, "test"))
        # Create an extra folder in the dst folder
        os.mkdir(os.path.join(self.dst, "extra"))
        # Run the sync_folders function
        self.syncer.sync_folders(self.src, self.dst)
        # Verify that the extra folder was removed from the dst folder
        self.assertEqual(filecmp.dircmp(self.src, self.dst).left_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).right_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_dirs, ["test"])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_files, [])

    def test_src_modified_folder(self):
        # Create a folder in both the src and dst folders
        os.mkdir(os.path.join(self.src, "test"))
        shutil.copytree(os.path.join(self.src, "test"), os.path.join(self.dst, "test"))
        # Modify the folder in the src folder by adding a file
        open(os.path.join(self.src, "test", "test.txt"), "w").close()
        # Run the sync_folders function
        self.syncer.sync_folders(self.src, self.dst)
        # Verify that the modified folder was copied to the dst folder
        self.assertEqual(filecmp.dircmp(self.src, self.dst).left_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).right_only, [])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_dirs, ["test"])
        self.assertEqual(filecmp.dircmp(self.src, self.dst).common_files, [])
        self.assertTrue(os.path.exists(os.path.join(self.dst, "test", "test.txt")))


if __name__ == "__main__":
    unittest.main()
