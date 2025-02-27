from os import listdir
from os.path import isfile, join

class DataStore:
    ext = ".fa"
    def __init__(self, data_path, extension=".fa"):
        self.basedir=data_path
        if extension is not None:
            self.ext = extension

    def get_data_files(self):
        files = [f for f in listdir(self.basedir) if f.endswith(self.ext) and isfile(join(self.basedir, f))]
        return files
    
    def absolute_path(self, filename):
        return join(self.basedir, filename)
        
    def exists(self, filename):
        return isfile(self.absolute_path(filename))
