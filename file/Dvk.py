import json
from processing.StringProcessing import extend_int
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
        self.set_artist()
        self.set_time()
        
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
            dvk_info["artists"] = self.get_artists()
            dvk_info["time"] = self.get_time()
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
                        self.set_artists(data["info"]["artists"])
                        self.set_time(data["info"]["time"])
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
            
    def get_title(self) -> str:
        """
        Returns the title for the current DVK file.
        
        Returns:
            str: DVK title
        """
        return self.title
    
    def set_artist(self, artist_str:str=None):
        """
        Sets the artists for the current DVK file for just a single artist.
        
        Parameters:
            artist_str (str): DVK Artist
        """
        a_list = [artist_str]
        self.set_artists(a_list)
    
    def set_artists(self, artist_list:list=None):
        """
        Sets the artists for the current DVK file.
        
        Parameters:
            artist_list (list): DVK artists
        """
        if artist_list == None:
            self.artists = []
        else:
            artist_set = set(artist_list)
            self.artists = list(artist_set)
            count = 0
            while count < len(self.artists):
                if self.artists[count] == None or self.artists[count] == 0:
                    del self.artists[count]
                else:
                    count = count + 1
                    
            self.artists = sorted(self.artists)
            
    def get_artists(self) -> list:
        """
        Returns a list of artists for the current DVK file.
        
        Returns:
            list: DVK artists
        """
        return self.artists
    
    def set_int_time(self, year_int:int=0, month_int:int=0, day_int:int=0, hour_int:int=0, minute_int:int=0):
        """
        Sets the time published for the current DVK file using ints representing individual units of time.
        
        Parameters:
            year_int (int): Int value of year published
            month_int (int): Int value of month published
            day_int (int): Int value of day published
            hour_int (int): Int value of hour published
            minute_int (int): Int value of minute published
        """
        if (year_int == None or year_int < 1 or
            month_int == None or month_int < 1 or month_int > 12 or
            day_int == None or day_int < 1 or day_int > 31 or
            hour_int == None or hour_int < 0 or hour_int > 23 or
            minute_int == None or minute_int < 0 or minute_int > 59):
            self.time = "0000/00/00|00:00"
        else:
            self.time = extend_int(year_int, 4) + "/" + extend_int(month_int, 2) + "/" + extend_int(day_int, 2) + "|" + extend_int(hour_int, 2) + ":" + extend_int(minute_int, 2)

    """
    Sets the time published for the current DVK file using a formatted time string.
    If time string is invalid, sets the date to 0000/00/00|00:00
    
    Parameters:
        time_str (str): String representation of time published. Should be formatted: YYYY/MM/DD/hh/mm
    """
    def set_time(self, time_str:str=None):
        if time_str == None or not len(time_str) == 16:
            self.time = "0000/00/00|00:00"
        else:
            try:
                self.set_int_time(int(time_str[0:4]), int(time_str[5:7]), int(time_str[8:10]), int(time_str[11:13]), int(time_str[14:16]))
            except ValueError:
                self.time = "0000/00/00|00:00"
 
    def get_time(self) -> str:
        """
        Returns the time published for the current DVK file.
        
        Reuturns:
            str: Time string of the time published for the DVK file
        """
        return self.time
    