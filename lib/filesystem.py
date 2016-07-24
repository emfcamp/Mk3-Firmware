### Author: EMF Badge team
### Description: Small set of micropython specific filesystem helpers
### License: MIT

import os

def get_app_foldername(path):
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
	
def get_app_attribute(path, attribute):
	if not is_file(path):
		return ""
	rv = ""
	attribute = attribute.lower()
	try:
		with open(path) as f:
			while True:  ## ToDo: set the max lines to loop over to be 20 or so
				l = f.readline()
				if l.startswith("### "):
					kv = l[4:].split(":",1)
					if len(kv) >= 2:
						if (kv[0].strip().lower() == attribute):
							rv = kv[1].strip()
							break;
				else:
					break
				
	except OSError as e:
		return ""
	return rv

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