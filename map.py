#importing packages

import openrouteservice
from openrouteservice.directions import directions
import customtkinter
from tkintermapview import TkinterMapView

customtkinter.set_default_color_theme("blue")

coords = [(-1.540704504417448,53.806167806881845),(-1.5358874132664084,53.80426084639122)]

client = openrouteservice.Client(key='5b3ce3597851110001cf6248b61898f56c394160be8a77936e312a7a') # Specify your personal API key
routes = directions(client, coords) # Now it shows you all arguments for .directions

def extract_coordinates_from_response(response):
    try:
        coordinates = []
        for step in response['routes'][0]['segments'][0]['steps']:
            if 'way_points' in step:
                coordinates.append(step['way_points'])
        
        # Check if there are any coordinates to extract
        if coordinates:
            # Flatten the list and convert the coordinates to a list of tuples with (longitude, latitude)
            coordinates = [(coord[1], coord[0]) for sublist in coordinates for coord in sublist]

        return coordinates
    except (KeyError, IndexError):
        return []


# Extract and print the coordinates
coordinates_only = extract_coordinates_from_response(routes)
print(coordinates_only)

#Creating the app class
class App(customtkinter.CTk):
    
    #Configuring the app
    APP_NAME = "Uber_Transport_SS"
    WIDTH = 800
    HEIGHT = 500
    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        #Configuring the window
        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)
        
        #Defining what happens when the app is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        #Different ways of quitting application by calling the function 'on_closing'

        self.marker_list = []
        #creates empty list 

        #creates two customtkinter frames 

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        #left column does not resize when window is resized, howecer right column and row is resized to be more proportionate

        #========= left frame =========

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        #left frame is aligned

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")
        #right frame is aligned 


        self.frame_left.grid_rowconfigure(2, weight=1)
        #makes the 3rd row expand when there is space avaliable e.g. when parent widget is resized 

        
        #Creating a button for adding a marker on the map
        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set Marker",
                                                command=self.set_marker_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        #Creating a button for clearing all the markers from the map
        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        #A label and option menu for changing tile servers (Google maps and google satellite)
        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=[ "Google normal", "Google satellite"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        #A label and option menu for changing between light, dark or system theme
        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        #Configuring which rows and columns will resize when the window is resized
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        #Creating an instance of the TkinterMapView class and setting the tile server
        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        #Creating an entry feild so that users can type in where they want to search up. The search_event function gets the text from this entry
        self.entry = customtkinter.CTkEntry(master=self.frame_right,placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)
        #search_event function is called when Enter key is pressed 

        #creates a button which calls the search_event function in order to change location on map by search
        self.button_5 = customtkinter.CTkButton(master=self.frame_right, text="Search",width=90,command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_address("Leeds")
        self.appearance_mode_optionemenu.set("Dark")

    #Gets the text from the entry and sets the map position to the place the user searched up
    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    #set a marker at a specific position
    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))
        if len(self.marker_list) == 2:
            path_1 = self.map_widget.set_path([self.marker_list[0].position, self.marker_list[1].position])
            print(self.marker_list[0].position)
            print(self.marker_list[1].position)
 
    #clears the placed marker
    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    #ability to change from dark or light mode
    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    #changes the tile server (either google maps or google satellite)
    def change_map(self, new_map: str):
        if new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    #terminates application
    def on_closing(self, event=0):
        self.destroy()

    
      



   