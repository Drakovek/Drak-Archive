import json
from pathlib import Path
from processing.StringProcessing import extend_int
from processing.ListProcessing import clean_list
from processing.HtmlProcessing import add_escapes_to_html

class Dvk:
    """
    Class for handling DVK files.
    
    Attributes:
        dvk_file (str): File path of the current DVK file
        id (str): ID of the current DVK file
        title (str): Title of the current DVK file
        artists (list): List of artists for the current DVK file
        time (str): Time of publication for the current DVK file (YYYY/MM/DD|hh:mm)
        web_tags (list): List of web tags for the current DVK file
        description (str): Description of the current DVK file
        page_url (str): Page URL of the current DVK file
        direct_url (str): Direct URL of the current DVK file
        secondary_url (str): Secondary URL of the current DVK file
    """
    def __init__(self, file_path:str=""):
        """
        Initializes all DVK values, reading from a DVK file, if given.
        """
        #CLEAR DVK VALUES
        self.dvk_file = ""
        self.set_file(file_path)
        self.clear_dvk()
        
        if not self.get_file() == None:
            self.read_dvk()
    
    def clear_dvk(self):
        """
        Sets all DVK data to their default values.
        """
        self.set_id()
        self.set_title()
        self.set_artist()
        self.set_time()
        self.set_web_tags()
        self.set_description()
        #WEB
        self.set_page_url()
        self.set_direct_url()
        self.set_secondary_url()
        
    def write_dvk(self):
        """
        Writes DVK data to the currently set DVK file.
        """
        if not self.get_file() == None:
            data = dict()
            data["file_type"] = "dvk"
            data["id"] = self.get_id()
            
            dvk_info = dict()
            dvk_info["title"] = self.get_title()
            dvk_info["artists"] = self.get_artists()
            if not self.get_time() == "0000/00/00|00:00":
                dvk_info["time"] = self.get_time()
            if len(self.get_web_tags()) > 0:
                dvk_info["web_tags"] = self.get_web_tags()
            if len(self.get_description()) > 0:
                dvk_info["description"] = self.get_description()
            data["info"] = dvk_info
            
            dvk_web = dict()
            dvk_web["page_url"] = self.get_page_url()
            if len(self.get_direct_url()) > 0:
                dvk_web["direct_url"] = self.get_direct_url()
            if len(self.get_secondary_url()) > 0:
                dvk_web["secondary_url"] = self.get_secondary_url()
            data["web"] = dvk_web
             
            #WRITE
            try:
                with open(self.get_file().absolute(), "w") as out_file:
                    json.dump(data, out_file)
                
            except IOError as e:
                print("File error: " + str(e))
    
    def read_dvk(self):
        """
        Reads DVK data from the currently set DVK file.
        """
        self.clear_dvk()
        if not self.get_file() == None and self.get_file().is_file():
            try:
                with open(self.get_file().absolute()) as in_file:
                    data = json.load(in_file)
                    if data["file_type"] == "dvk":
                        self.set_id(data["id"])
                        self.set_title(data["info"]["title"])
                        self.set_artists(data["info"]["artists"])
                        try:
                            self.set_time(data["info"]["time"])
                        except:
                            self.set_time()
                        try:
                            self.set_web_tags(data["info"]["web_tags"])
                        except:
                            self.set_web_tags()
                        try:
                            self.set_description(data["info"]["description"])
                        except:
                            self.set_description()
                            
                        self.set_page_url(data["web"]["page_url"])
                        try:
                            self.set_direct_url(data["web"]["direct_url"])
                        except:
                            self.set_direct_url()
                        try:
                            self.set_secondary_url(data["web"]["secondary_url"])
                        except:
                            self.set_secondary_url()
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
            self.dvk_file = None
        else:
            self.dvk_file = Path(file_path)
    
    def get_file(self) -> Path:
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
            self.artists = sorted(clean_list(artist_list))
            
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
        
        Returns:
            str: Time string of the time published for the DVK file
        """
        return self.time
    
    def set_web_tags(self, web_tag_list:list=None):
        """
        Sets the web tags for the current DVK file.
        
        Parameters:
            web_tag_list (list): DVK web tags
        """
        if web_tag_list == None:
            self.web_tags = []
        else:
            self.web_tags = clean_list(web_tag_list)
            
        
    def get_web_tags(self) -> list:
        """
        Returns the web tags for the current DVK file.
        
        Returns:
            list: DVK web tags
        """
        return self.web_tags
    
    def set_description(self, description_str:str=None):
        """
        Sets the description for the current DVK file.
        
        Parameters:
            description_str (str): DVK description
        """
        self.description = add_escapes_to_html(description_str)
        
    def get_description(self) -> str:
        """
        Returns the description for the current DVK file.
        
        Returns:
            str: DVK description
        """
        return self.description
    
    def set_page_url(self, page_url_str:str=None):
        """
        Sets the page URL for the current DVK file.
        
        Parameters:
            page_url_str (str): Page URL
        """
        if page_url_str == None:
            self.page_url = ""
        else:
            self.page_url = page_url_str
        
    def get_page_url(self) -> str:
        """
        Returns the page URL for the current DVK file.
        
        Returns:
            str: Page URL
        """
        return self.page_url
    
    def set_direct_url(self, direct_url_str:str=None):
        """
        Sets the direct media URL for the current DVK file.
        
        Parameters:
            direct_url_str (str): Direct media URL
        """
        if direct_url_str == None:
            self.direct_url = ""
        else:
            self.direct_url = direct_url_str
        
    def get_direct_url(self) -> str:
        """
        Returns the direct media URL for the current DVK file.
        
        Returns:
            str: Direct media URL
        """
        return self.direct_url
    
    def set_secondary_url(self, secondary_url_str:str=None):
        """
        Sets the secondary media URL for the current DVK file.
        
        Parameters:
            secondary_url_str (str): Secondary media URL
        """
        if secondary_url_str == None:
            self.secondary_url = ""
        else:
            self.secondary_url = secondary_url_str
        
    def get_secondary_url(self) -> str:
        """
        Returns the secondary media URL for the current DVK file.
        
        Returns:
            str: Secondary media URL
        """
        return self.secondary_url
    