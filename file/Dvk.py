import json
class Dvk:
    """
    Class for handling DVK files.
    
    Attributes:
        dvk_file (str): 
        id (str):
        title (str):
    """
    def __init__(self, file_path:str=""):
        """
        Initializes all DVK values, reading from a DVK file, if given.
        """
        #CLEAR DVK VALUES
        self.dvk_file = ""
        self.set_file(file_path)
        self.clear_dvk()
        
        if not self.get_file() == "":
            self.read_dvk()
    
    def clear_dvk(self):
        """
        Sets all DVK data to their default values.
        """
        self.set_id()
        self.set_title()
        
    def write_dvk(self):
        """
        Writes DVK data to the currently set DVK file.
        """
        if not self.get_file() == "":
            data = dict()
            data["file_type"] = "dvk"
            data["id"] = self.get_id()
            
            dvk_info = dict()
            dvk_info["title"] = self.get_title()
            data["info"] = dvk_info
             
            #WRITE
            try:
                with open(self.get_file(), "w") as out_file:
                    json.dump(data, out_file)
                
            except IOError as e:
                print("File error: " + str(e))
    
    def read_dvk(self):
        """
        Reads DVK data from the currently set DVK file.
        """
        self.clear_dvk()
        if not self.get_file() == "":
            try:
                with open(self.get_file()) as in_file:
                    data = json.load(in_file)
                    if data["file_type"] == "dvk":
                        self.set_id(data["id"])
                        self.set_title(data["info"]["title"])
            except:
                print("Error reading DVK")
                self.clear_dvk()
                
    def set_file(self, file_path:str=None):
        """
        Sets the current path for the DVK file.
        
        Parameters:
            file_path (str): Path for the DVK file
        """
        if file_path == None:
            self.dvk_file = ""
        else:
            self.dvk_file = file_path
    
    def get_file(self) -> str:
        """
        Returns the current path of the DVK file.
        
        Returns:
            str: DVK file path
        """
        return self.dvk_file
        
    def set_id(self, id_str:str=None):
        """
        Sets the ID for the current DVK file.
        
        Parameters:
            id_str (str): DVK ID
        """
        if id_str == None:
            self.id = ""
            
        else:
            self.id = id_str.upper()
        
    def get_id(self) -> str:
        """
        Returns the ID for the current DVK file.
        
        Returns:
            str: DVK ID
        """
        return self.id.upper()
    
    def set_title(self, title_str:str=None):
        """
        Sets the title for the current DVK file.
        
        Parameters:
            title_str (str): DVK title
        """
        if title_str == None:
            self.title = ""
        else:
            self.title = title_str
            
    def get_title(self):
        """
        Returns the title for the current DVK file.
        
        Returns:
            str: DVK title
        """
        return self.title
    