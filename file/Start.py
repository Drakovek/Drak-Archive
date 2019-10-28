from pathlib import Path
from file.Dvk import Dvk

dvk = Dvk()

file_path = Path("test.dvk").absolute()
print(file_path)
dvk.set_file(file_path)

dvk.set_id("id123")
dvk.set_title("This is a title")
dvk.set_artists(["Artist 2", "Artist 1"])
dvk.set_int_time(2017, 10, 27, 5, 10)
dvk.set_web_tags(["Some", "tags", "here"])
dvk.set_description("This is a description! :)")

dvk.set_page_url("Https://pageurl.com")
dvk.set_direct_url("http://DirectUrl.com")
dvk.set_secondary_url("http://Secondaryurl.COM")

dvk.set_media_file("image.png")
dvk.write_dvk()
