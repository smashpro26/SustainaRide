import customtkinter 
import requests
import json
from Driverpopup import  DriverPanel
from Passengerpopup import PassengerPanel
import tkinter as tk

#The class for picking others up (the driver)
class PickOthers(customtkinter.CTkToplevel):
    def __init__(self,driver_start_coordinates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #configuring the window
        self.driver_start_coordinates = driver_start_coordinates
        self.geometry("400x300")

        #entry for the driver's name
        self.enter_name= customtkinter.CTkEntry(master=self,placeholder_text="Enter your name: ")
        self.enter_name.grid(row=0, column=0, sticky='nsew')

        #entry for driver's age
        self.enter_age = customtkinter.CTkEntry(master=self,placeholder_text="Enter your age: ")
        self.enter_age.grid(row=1, column=0, sticky='nsew')

        #entry for driver's numberplate
        self.enter_numplate = customtkinter.CTkEntry(master=self,placeholder_text="Enter your car numberplate: ")
        self.enter_numplate.grid(row=2, column=0, sticky='nsew')

        #Slider for search range in miles
        self.driver_pickup_range = "1"
        self.slider_variable = tk.IntVar()
        self.distance_slider = customtkinter.CTkSlider(master=self,from_=1, to=15,variable=self.slider_variable, command=self.update_slider_label)
        self.distance_slider.grid(row=3, column=0, sticky='ew')

        #displaying the pickup range to the user
        self.distance_label = customtkinter.CTkLabel(master=self,text="pickup range: 1 mile(s)")
        self.distance_label.grid(row=3, column=1, sticky='nsew')

        #button for calling pasenger popup once all details have been entered correctly
        self.start_search_button = customtkinter.CTkButton(master=self,text="Start Searching", command=self.wait_to_find_passenger)
        self.start_search_button.grid(row=4, column=0, sticky='nsew')
        
        self.grid_rowconfigure(0, weight=0)  # label row
        self.grid_rowconfigure(1, weight=1)  # enter_name row
        self.grid_rowconfigure(2, weight=1)  # enter_age row
        self.grid_rowconfigure(3, weight=1)  # enter_numplate row
        
    #updating the label's value to show the value of the slider
    def update_slider_label(self, _):
        self.driver_pickup_range = str(int(self.distance_slider.get()))
        self.distance_label.configure(text="pickup range: "+self.driver_pickup_range  +" mile(s)")    
    
    #function for handling what happens after the button is pressed
    def wait_to_find_passenger(self):
        self.name = self.enter_name.get()
        self.age = self.enter_age.get()
        self.numplate = self.enter_numplate.get()
        
        #Checking that the data has been put in properly
        if self.name != "" and self.numplate != "" and int(self.age) >= 17:
            self.data_to_send = {
                "name": self.name, 
                "age": self.age, 
                "numplate": self.numplate,
                "driver_start_coordinates": self.driver_start_coordinates,
                "driver_pickup_range": self.driver_pickup_range
                } 
            #checking for errors using the try except
            try:
                response = requests.post('http://surveyer.pythonanywhere.com/post_driver_data', json=self.data_to_send)
                response.raise_for_status()  # Raise an exception for HTTP errors
                response_data = response.json()
                print(response.status_code)
                DriverPanel(self.name) 
            except requests.exceptions.RequestException as e:
                 print(f"Request error: {e}")

#creates and instance of the class above which creates a popup window
def PickUpOthers(driver_start_coordinates):
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = PickOthers(driver_start_coordinates)
    else:
        toplevel_window.focus()  # if window exists focus it
    
    
#class for people getting picked (passengers)
class GetPicked(customtkinter.CTkToplevel):
    def __init__(self,passenger_start_coordinates, passenger_end_coordinates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #configuring the window and initializing variables
        self.passenger_start_coordinates = passenger_start_coordinates
        self.passenger_end_coordinates = passenger_end_coordinates
        self.geometry("400x300")
        
        #entry for passenger name
        self.enter_name= customtkinter.CTkEntry(master=self,placeholder_text="Enter your name: ")
        self.enter_name.grid(row=0, column=0, sticky='nsew')

        #entry for passenger age
        self.enter_age = customtkinter.CTkEntry(master=self,placeholder_text="Enter your age: ")
        self.enter_age.grid(row=1, column=0, sticky='nsew')

        #button to start the search process
        self.start_search_button = customtkinter.CTkButton(master=self,text="Start Searching", command=self.wait_to_find_driver)
        self.start_search_button.grid(row=3, column=0, sticky='nsew')

        #configuring the row/column weights
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_rowconfigure(2, weight=1)
    
    #function for handing what happens when the user presses the button
    def wait_to_find_driver(self):
        self.name = self.enter_name.get()
        self.age = self.enter_age.get() 

        #checking if the values input by the user are valid
        if self.name != "" and self.age != "" and int(self.age) >= 13:
            self.data_to_send = {
                "name" : self.name, 
                "age" : self.age,
                "passenger_start_coordinates": self.passenger_start_coordinates,
                "passenger_end_coordinates": self.passenger_end_coordinates
                }

            #Try to post the passenger's data
            try:
                response = requests.post('http://surveyer.pythonanywhere.com/post_passenger_data', json=self.data_to_send)
                response.raise_for_status()  # Raise an exception for HTTP errors
                response_data = response.json()
                print(response.status_code)
                PassengerPanel(self.data_to_send)
            except requests.exceptions.RequestException as e:
                 print(f"Request error: {e}")
        
#creates an instance of the class above, this displays a popup
def GetPickedUp(passenger_start_coordinates, passenger_end_coordinates):
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = GetPicked(passenger_start_coordinates, passenger_end_coordinates)  # create window if its None or destroyed
    else:
        toplevel_window.focus()  # if window exists focus it













