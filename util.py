import os
import environ as env
import shutil
import pickle

def makeFolder(folderName):
    dirpath = env.DBPATH + folderName
    #dirpath = rootdirpath + "/result/"

    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        """
        if os.path.exists(dirpath + "old_result") and os.path.isdir(dirpath + "old_result"):
            shutil.rmtree(dirpath + "old_result")
        shutil.move(dirpath, dirpath + "old_result")
        """

    os.makedirs(dirpath)
    return dirpath

def save_obj(obj, path):
    with open(path + '.pkl', 'wb') as f:
        pickle.dump(obj, f, 0)

def load_obj(path):
    with open(path + '.pkl', 'rb') as f:
        return pickle.load(f)