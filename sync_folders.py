"""
This script contains a SyncFolders class that can be used to synchronize the contents of two folders.
"""
import os
import time
import argparse
import logging
import filecmp
import shutil


class SyncFolders:
    def __init__(self, src, dst, interval, logfile):
        """Initialize folder synchronization.

        :param src: The source folder to synchronize.
        :type src: String
        :param dst: The replica folder to synchronize with the source.
        :type dst: String
        :param interval: The synchronization interval in seconds.
        :type interval: int
        :param logfile: The file to log synchronization operations to.
        :type logfile: String
        """
        self.src = src
        self.dst = dst
        self.interval = interval
        self.logfile = logfile

        # Create directories if doesn't exist
        if not os.path.exists(src):
            os.makedirs(src)
        if not os.path.exists(dst):
            os.makedirs(dst)

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            filename=self.logfile,
            filemode="w",
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def sync_folders(self, src, dst):
        """Synchronize the contents of the src folder with the dst folder.

        :param src: The source folder to synchronize.
        :type src: String
        :param dst: The replica folder to synchronize with the source.
        :type dst: String
        """
        # Compare the contents of the two folders
        comparison = filecmp.dircmp(src, dst)

        # Iterate over the files in the src folder
        for name in comparison.left_only:
            src_path = os.path.join(src, name)
            dst_path = os.path.join(dst, name)
            # If it is a file, copy it to the dst folder
            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
                logging.info(f"Copied file {src_path} to {dst_path}")
                print(f"Copied file {src_path} to {dst_path}")
            # If it is a subfolder, create it in the dst folder
            elif os.path.isdir(src_path):
                os.mkdir(dst_path)
                logging.info(f"Created folder {dst_path}")
                print(f"Created folder {dst_path}")
                self.sync_folders(src_path, dst_path)

        # Iterate over the common files in both folders
        for name in comparison.common_files:
            src_path = os.path.join(src, name)
            dst_path = os.path.join(dst, name)
            # Check if the file has been modified in the src folder
            if filecmp.cmp(src_path, dst_path, shallow=False):
                # If not, skip it
                continue
            # If the file has been modified, copy it to the dst folder
            shutil.copy(src_path, dst_path)
            logging.info(f"Updated file {src_path} in {dst_path}")
            print(f"Updated file {src_path} in {dst_path}")

        # Iterate over the common subfolders in both folders
        for name in comparison.common_dirs:
            src_path = os.path.join(src, name)
            dst_path = os.path.join(dst, name)
            self.sync_folders(src_path, dst_path)

        # Iterate over the files and folders that exist in the dst but not in the src
        for name in comparison.right_only:
            dst_path = os.path.join(dst, name)
            # If it is a file, delete it from the dst folder
            if os.path.isfile(dst_path):
                os.remove(dst_path)
                logging.info(f"Removed file {dst_path}")
                print(f"Removed file {dst_path}")
            # If it is a folder, delete it and its contents from the dst folder
            elif os.path.isdir(dst_path):
                shutil.rmtree(dst_path)
                logging.info(f"Removed folder {dst_path}")
                print(f"Removed folder {dst_path}")


if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="the source folder to synchronize")
    parser.add_argument("replica", help="the replica folder to synchronize with the source")
    parser.add_argument("interval", type=int, help="the synchronization interval in seconds")
    parser.add_argument("logfile", help="the file to log synchronization operations to")
    args = parser.parse_args()

    # Create a SyncFolders object
    syncer = SyncFolders(args.source, args.replica, args.interval, args.logfile)

    print("press cntrl+c to exit program.")

    # Start synchronization
    try:
        while True:
            syncer.sync_folders(syncer.src, syncer.dst)
            time.sleep(syncer.interval)
    except KeyboardInterrupt:
        print("program terminated.")
