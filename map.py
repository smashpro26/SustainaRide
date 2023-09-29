    #importing packages

from openrouteservice.directions import directions
import customtkinter
from tkintermapview import TkinterMapView
import directions
from llama_ai import get_answer
from Reversegeocode import reverse_geocode
from popup import PickUpOthers, GetPickedUp
from text_to_speech import play_text_as_audio, stop_audio_thread
import threading
import speech_recognizer

customtkinter.set_default_color_theme("blue")
#Creating the app class
class App(customtkinter.CTk):

    #Configuring the app
    APP_NAME = "SustainaRide"
    WIDTH = 1400
    HEIGHT = 800

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path_1 = None
        self.num_of_markers =0
        self.toggle_state = True

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
        self.grid_rowconfigure(2,weight = 0)
        #left column does not resize when window is resized, howecer right column and row is resized to be more proportionate

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        #left frame is aligned

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")
        #right frame is aligned 


        self.frame_left.grid_rowconfigure(2, weight=1)
        #makes the 3rd row expand when there is space avaliable e.g. when parent widget is resized 

        

        #========= left frame =========
        
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

        #creating a frame for holding carpooling elements
        self.carpool_frame = customtkinter.CTkFrame(master=self.frame_left)
        self.carpool_frame.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

        #creating a label for the carpooling frame
        self.carpool_label = customtkinter.CTkLabel(master=self.carpool_frame,text="Carpooling")
        self.carpool_label.grid(pady=(10, 0), padx=(20, 20), row=0, column=0)

        #Creating a button for people driving
        self.pick_others = customtkinter.CTkButton(master=self.carpool_frame, text="Pick others up", state="disabled",command=self.pick_others_up)
        self.pick_others.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        #Creating a button for passengers
        self.get_picked = customtkinter.CTkButton(master=self.carpool_frame, text="Get picked up", state = "disabled", command=self.get_picked_up)
        self.get_picked.grid(pady=(20, 20), padx=(20, 20), row=2, column=0)
        


        #A label and option menu for changing tile servers (Google maps and google satellite)
        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=[ "Google normal", "Google satellite"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=5, column=0, padx=(20, 20), pady=(10, 0))

        #A label and option menu for changing between light, dark or system theme
        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=(20, 20), pady=(10, 20))

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
        self.entry.grid(row=0, column=0, sticky="ew", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)
        #search_event function is called when Enter key is pressed 

        #creates a button which calls the search_event function in order to change location on map by search
        self.button_5 = customtkinter.CTkButton(master=self.frame_right, text="Search",width=90,command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_address("Leeds")
        self.appearance_mode_optionemenu.set("Dark")

        #==================== Frame right column ==============================
        
        self.right_column = customtkinter.CTkFrame(master=self)
        self.right_column.grid(row=0, column=2, sticky="nsew")  # Use sticky option
        self.grid_rowconfigure(0, weight=1)  # Configure the row to expand vertically
        self.right_column.grid_columnconfigure(0, weight=1)
        #self.right_column.grid_columnconfigure()
        self.right_column.grid_rowconfigure(3, weight=1)   

        #Text feild for asking the ai another question
        self.userinput_entry = customtkinter.CTkEntry(master= self.right_column, placeholder_text="Ask for extra details...")
        self.userinput_entry.grid(row=0, column=2, sticky = "ew",pady=(20, 0), padx=(20, 20),columnspan=2)
        self.userinput_entry.bind("<Return>", self.user_input)

        #Button for entering the user
        self.enter_button = customtkinter.CTkButton(master=self.right_column, text="Enter", command=self.user_input)
        self.enter_button.grid(row=1, column=2,sticky = "ew",pady=(20, 0), padx=(20, 20),columnspan=1)

        #Button for text to speech
        self.speak_button = customtkinter.CTkButton(master=self.right_column,state= "disabled",text="Speak text", command= self.text_to_speech)
        self.speak_button.grid(row=1, column=3,sticky = "ew",pady=(20, 0), padx=(20, 20))

        #Button for speech to text
        self.listen_button = customtkinter.CTkButton(master=self.right_column,text="Speech to text", state="normal", command=self.toggle_microphone)
        self.listen_button.grid(row=2, column=2,sticky = "ew",pady=(20, 0), padx=(20, 20))

        #frame for holding the label
        self.textframe = customtkinter.CTkScrollableFrame(master=self.right_column, label_text="Your Trip Planner",width=250)
        self.textframe.grid(pady=(20, 0), padx=(20, 20), row=3, column=2, columnspan=2, sticky="nsew")

        #label containing the response from the ai
        self.info_label = customtkinter.CTkLabel(master = self.textframe, anchor='e',text= " ",wraplength=295)
        self.info_label.grid(row=0, column=0, sticky="w")


    #Gets the text from the entry and sets the map position to the place the user searched up
    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())
        self.map_widget.adre
        self.map_widget.set_address()
    
    #set a marker at a specific position
    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        
        self.num_of_markers+=1
        if self.num_of_markers == 1:
            self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1],text="Start"))
            self.start_address = reverse_geocode(latitude=current_position[0], longitude= current_position[1])
        elif self.num_of_markers == 2:
            self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1],text="End"))
            self.latitude = current_position[0]
            self.longitude = current_position[1]
            self.end_address = reverse_geocode(latitude=current_position[0], longitude= current_position[1])
        
        #If the number of markers is greater than 2, get a response and show a route
        if len(self.marker_list) >= 2:
            
            self.start_and_end_point = [(self.marker_list[0].position[1],self.marker_list[0].position[0]),(self.marker_list[1].position[1],self.marker_list[1].position[0])]
            self.coords, self.distance = directions.extract_coordinates_from_response(self.start_and_end_point)
            self.path_1 = self.map_widget.set_path([self.marker_list[0].position, self.coords[0] ])
            #print(coords)
            self.start_and_end_point = [(self.marker_list[0].position),(self.marker_list[1].position)]
            for i in range(len(self.coords)):
                deg_x =self.coords[i][0]
                deg_y =self.coords[i][1]
                self.path_1.add_position(deg_x,deg_y) 
            self.ask_for_recommendation()
            self.pick_others.configure(state = "normal")
            self.get_picked.configure(state= "normal")
    


    #Function for asking the ai for a recommendation on the best mode of transport between 2 points            
    def ask_for_recommendation(self):
        prompt = "Recommend the ideal mode of transport (car and taxi are also options) for someone traveling between: " + self.start_address + " to " + self.end_address + " which has a distance of: " + str(self.distance) + " in meters (convert this to miles) with your response including the names of the places of start and end points and in bullet points containing the modes of transport in this format recommended: your recommendation (new line)other mode of transportation (new line)Other mode of transportation and the costs of the public transport modes"
        self.info_label.configure(text="Waiting for response...", anchor='w')

        def run_get_answer():
            result = get_answer(prompt)
            self.answer = result
            self.info_label.configure(text=result, anchor='w')
            print(str(self.start_address))
            print(str(self.end_address))
            self.speak_button.configure(state="normal")

        self.get_answer_thread = threading.Thread(target=run_get_answer)
        self.get_answer_thread.start()

    #Getting the answer from the ai for addtional questions
    def user_input(self,event=None):
        prompt = self.userinput_entry.get()
        self.answer = get_answer(prompt)
        self.info_label.configure(text=self.answer, anchor='w')
        
 
    #clears the placed marker(s) and path 
    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()
            self.path_1.delete()
        self.marker_list.clear()
        self.num_of_markers = 0
        self.pick_others.configure(state = "disabled")
        self.get_picked.configure(state= "disabled")
        self.speak_button.configure(state = "disabled")

    #converts ai text to speech
    def text_to_speech(self):
        play_text_as_audio(self.answer)
    
    #Toggles between mic on and off
    def toggle_microphone(self):
        if self.toggle_state:
            self.start_mic()
            self.toggle_state = False
        else:
            self.end_mic()
            self.toggle_state = True
    
    #Starts recording
    def start_mic(self):
        speech_recognizer.start_recording()
        self.listen_button.configure(text= "Stop Listening")
    
    #ends recording
    def end_mic(self):
        speech_recognizer.stop_recording("voice_recording.wav")
        self.listen_button.configure(text= "Start Listening")
        self.transcript = speech_recognizer.transcribe_audio("voice_recording.wav")
        self.answer = get_answer(self.transcript)
        self.info_label.configure(text=self.answer, anchor='w')
        self.speak_button.configure(state = "normal")

    
    #creates a popup window for picking others up
    def pick_others_up(self):
        PickUpOthers(self.marker_list[0].position)


    
    #creates a popup window for getting picked up
    def get_picked_up(self):
        GetPickedUp(self.marker_list[0].position,self.marker_list[1].position)
        

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
        self.drivers = []
        self.passengers = []
        self.accepted_drivers = []
        stop_audio_thread()
        self.destroy()

    
      



   