from os.path import join, basename, exists
from os import chdir
import tarfile
import glob
import logging
logging.basicConfig(level=logging.INFO)

def tar_compress(archive_name, source_dir, out_dir):

    """
    input: zip_file name, directory of the file you want to zip
    output: tar.gz file in current directory
    """

    with tarfile.open(join(out_dir, archive_name), "w:gz") as tar:
        chdir(source_dir)
        for file_name in glob.glob(source_dir):
            tar.add(file_name, basename(file_name))
    tar.close()


def errorhandler(filename, path):
    logging.info("Invalid zip type")

def tar_decompress(archive_name, file_path):

    """
    input: zip_file name, destination directory of decompressed files
    output: decompressed files in destination directory
    """

    dest_dir = join(file_path, archive_name)
    with tarfile.open(dest_dir, "r") as tar:
        tar.extractall(path=file_path)
    tar.close()


class ZipHandler():

    """Purpose is to do switch case for compressing and decompressing"""

    def __init__(self, output_filename, ztype='.tar.gz', flags=""):
        self.output_filename = output_filename
        self.ztype = ztype
        self.flags = flags

    def switch_compress(self, file_path, output_path):
        switcher = {
            ".tar.gz": tar_compress,
        }
        return switcher.get(self.ztype, errorhandler)(self.output_filename + self.ztype, file_path, output_path)

    def switch_decompress(self, output_path):
        switcher = {
            ".tar.gz": tar_decompress,
        }
        return switcher.get(self.ztype, errorhandler)(self.output_filename + self.ztype, output_path)

    def compressor(self, file_path, output_path):

        """
        input: file_path of the file you want to zip, name of the output zip file,
                zip type and flags
        output: zip a file in current directory
        """

        # check file_path existance
        if not exists(file_path):
            return {"error": "no {} file directory".format(file_path)}

        # select switch case and do compressing
        self.switch_compress(file_path, output_path)

    def decompressor(self, file_path, output_path):

        """
        input: file_path of the file you want to zip, name of the output zip file,
                zip type and flags
        output: zip a file in current directory
        """

        # check file_path existance
        if not exists(file_path):
            return {"error": "no {} file directory".format(file_path)}

        # select switch case and do decompressing
        self.switch_decompress(output_path)
