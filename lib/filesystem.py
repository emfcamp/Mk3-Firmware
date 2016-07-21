### Author: EMF Badge team
### Description: Small set of micropython specific filesystem helpers
### License: MIT

import os

def get_app_name(path):
	"""Gets the app name based on a path"""
	if not is_file(path):
		return ""
		
	s = path.split("/")
	if not (len(s) >= 2):
		return ""
	
	if s[0] == "examples":
		if s[-1].endswith(".py"):
			return ((s[-1])[:-3])
		else:
			return ""
	else:
		return s[-2]
	

def is_dir(path):
    """Checks whether a path exists and is a director"""
    try:
        return os.stat(path)[0] & 61440 == 16384
    except OSError as e:
        if e.args[0] == 2:
            return False
        else:
            raise e

def is_file(path):
    """Checks whether a path exists and is a regular file"""
    try:
        return os.stat(path)[0] & 61440 == 32768
    except OSError as e:
        if e.args[0] == 2:
            return False
        else:
            raise e

def exists(path):
    """Checks whether a path exists"""
    try:
        os.stat(path)
        return True
    except OSError as e:
        if e.args[0] == 2:
            return False
        else:
            raise e