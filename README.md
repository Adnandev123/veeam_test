# veeam_test

Run: ``python sync_folders.py src dst interval logfile``

Run(for test): ``python test_sync_folders.py``

Note: This repository contains git actions for CI which will run the unit tests automatically if any new push or pull request merged.

## sync_folders.py:

This script contains a ``SyncFolders`` class that can be used to synchronize the contents of two folders. The class has a ``__init__`` method that takes four arguments:

* ``src``: the source folder to synchronize.
* ``dst``: the replica folder to synchronize with the source.
* ``interval``: the synchronization interval in seconds.
* ``logfile``: the file to log synchronization operations to.

The ``__init__`` method sets up the class instance with these four arguments and also creates the ``src`` and ``dst`` folders if they do not exist. It also sets up logging using the logging module.

The ``SyncFolders`` class has a sync_folders method that takes two arguments:

* ``src``: the source folder to synchronize.
* ``dst``: the replica folder to synchronize with the source.

This method compares the contents of the two folders using the ``filecmp`` module and synchronizes them by iterating over the files and folders in the ``src`` folder and:

* Copying new files and folders from the ``src`` folder to the ``dst`` folder.
* Updating modified files in the ``dst`` folder with the corresponding files from the ``src`` folder.
* Removing files and folders from the ``dst`` folder that do not exist in the ``src`` folder.

The script also contains a block of code that sets up command line arguments using the argparse module and creates a ``SyncFolders`` object using these arguments. It then enters an infinite loop where it synchronizes the ``src`` and ``dst`` folders every ``interval`` seconds using the time module's sleep function.


## test_sync_folders.py:

This script contains a test suite for the ``SyncFolders`` class defined in the ``sync_folders`` module. The test suite is defined by the ``TestSyncFolders`` class, which is a subclass of the unittest.TestCase class.

The ``TestSyncFolder``s class has following test methods:

* ``test_same_folders``: This test verifies that the ``sync_folders`` function does not make any changes to the folders if they are already synchronized.
* ``test_src_empty``: This test verifies that the ``sync_folders`` function removes files from the ``dst`` folder if they do not exist in the ``src`` folder.
* ``test_src_has_new_file``: This test verifies that the ``sync_folders`` function copies new files from the ``src`` folder to the ``dst`` folder.
* ``test_src_modified_file``: This test verifies that the ``sync_folders`` function updates modified files in the dst folder with the corresponding files from the ``src`` folder.
* ``test_src_has_new_folder``: This test verifies that the ``sync_folders`` function copies new folders from the ``src`` folder to the ``dst`` folder.
* ``test_dst_has_extra_file``: This method tests the case where the destination directory has an extra file that is not in the source directory.
* ``test_dst_has_extra_folder``: This method is similar to the ``test_dst_has_extra_file`` method, but it tests the case where the destination directory has an extra subdirectory.
* ``test_src_modified_folder``: This method tests the case where a subdirectory in the source directory has been modified by adding a new file.

The ``TestSyncFolders`` class also has a ``setUp`` method that is run before each test case. This method creates a temporary directory and sets up the ``src`` and ``dst`` folders for testing. It also creates a ``SyncFolders`` object for testing.

The ``TestSyncFolders`` class also has a ``tearDown`` method that is run after each test case. This method deletes the temporary directory.
