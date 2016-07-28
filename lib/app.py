### Author: EMF Badge team
### Description: Model for TiLDA apps
### License: MIT
import os, ure
import filesystem

EMF_USER = "emf"
USER_NAME_SEPARATOR = "~"
ATTRIBUTE_MATCHER = ure.compile("^\s*###\s*([^:]*?)\s*:\s*(.*)\s*$") # Yeah, regex!

class App:
    """Models an app and provides some helper functions"""
    def __init__(self, folder_name):
        self.folder_name = self.name = folder_name
        self.user = EMF_USER
        if USER_NAME_SEPARATOR in folder_name:
            [self.user, self.name] = folder_name.split(USER_NAME_SEPARATOR, 1)

        self._attributes = None # Load lazily

    @property
    def folder_path(self):
        return "apps/" + self.folder_name

    @property
    def main_path(self):
        return self.folder_path + "/main.py"

    @property
    def loadable(self):
        return filesystem.is_file(self.main_path)

    @property
    def attributes(self):
        if self._attributes == None:
            self._attributes = {}
            if self.loadable:
                with open(self.main_path) as file:
                    for line in file:
                        match = ATTRIBUTE_MATCHER.match(line)
                        if match:
                            self._attributes[match.group(1).strip().lower()] = match.group(2).strip()
                        else:
                            break
        return self._attributes

    def get_attribute(self, attribute, default=None):
        """Returns the value of an attribute, or a specific default value if attribute is not found or main.py doesn't exist"""
        attribute = attribute.lower() # attributes are case insensitive
        if attribute in self.attributes:
            return self.attributes[attribute]
        else:
            return default

def app_by_name_and_user(name, user):
    """Returns an user object"""
    if user.lower() == EMF_USER:
        return App(name)
    else:
        return App(user + USER_NAME_SEPARATOR + name)
