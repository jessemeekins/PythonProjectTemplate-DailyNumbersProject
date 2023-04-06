#%%
import sys
sys.path.insert(0, "..")

from ProjectClasses.FilePaths import DefinedFilePaths
import os

def test_local_file_path(var):
    path_object = DefinedFilePaths()
    path_to_test = path_object.local_file_path()
    inpath = path_to_test.get(var, None)
    return os.path.exists(inpath)

path=test_local_file_path('filepath') 
export=test_local_file_path('exports')

print(path,export)