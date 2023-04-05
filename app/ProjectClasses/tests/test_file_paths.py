#%%

from ProjectClasses.FilePaths import DefinedFilePaths
import os

def test_local_file_path():
    path_object = DefinedFilePaths()
    path_to_test = path_object.local_file_path()
    assert os.path.exists(path_to_test)
