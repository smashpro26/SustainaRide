import customtkinter
import requests
from Reversegeocode import reverse_geocode


class AcceptPassenger(customtkinter.CTkToplevel):
    def __init__(self,passenger_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #initialising variables and configuring the window
        self.passenger_info = passenger_info
        self.geometry("500x200")
        self.title("Passenger Requests")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        #Frame for holding the ui
        self.passenger_requests_frame = customtkinter.CTkScrollableFrame(master=self,label_text="Incoming Passenger Request",)
        self.passenger_requests_frame.grid(row=0, column=0,sticky = "nsew")
        
        #geting the start coords of the passenger
        self.passenger_start_lat = self.passenger_info.get('passenger_start_coordinates')[0]
        self.passenger_start_lon = self.passenger_info.get('passenger_start_coordinates')[1]

        #getting the end coords of the passenger
        self.passenger_end_lat = self.passenger_info.get('passenger_end_coordinates')[0]
        self.passenger_end_lon = self.passenger_info.get('passenger_end_coordinates')[1]

        #Using reverse geocoding to return the address of the coordinates
        self.start_address = reverse_geocode(self.passenger_start_lat,self.passenger_start_lon)
        self.end_address = reverse_geocode(self.passenger_end_lat, self.passenger_end_lon)

        #Displays the passengers info
        self.passenger_label = customtkinter.CTkLabel(master = self.passenger_requests_frame,wraplength=490,text= f"Passenger Name: {self.passenger_info['passenger_name']}, " f"Age: {self.passenger_info['passenger_age']}, "f"Pickup Location: {self.start_address}, "f"Final Destination: {self.end_address}")
        self.passenger_label.grid(pady=(20, 0), padx=(20, 20), row=0, column=0,sticky = "ew")

        #accepting the passenger
        self.accept_button = customtkinter.CTkButton(master=self.passenger_requests_frame, text="Accept", command=self.accept_incoming_passenger)
        self.accept_button.grid(row=1, column=0,pady=(20, 0), padx=(0, 20),sticky = "w")

        #declining the passenger
        self.decline_button = customtkinter.CTkButton(master = self.passenger_requests_frame,text="Decline")
        self.decline_button.grid(row=2, column=0,pady=(20, 0), padx=(0, 20),sticky = "w")

    #posting passenger info to passenger accepted so that the passenger knows that they have been accepted
    def accept_incoming_passenger(self):
        self.accepted_passenger_info = {
            'passenger_name': self.passenger_info['passenger_name'],
            'passengers_age': self.passenger_info['passenger_age'],
            'passenger_end_coordinates' : self.passenger_info['passenger_end_coordinates'],
            'driver_name': self.passenger_info['driver_name'],
            'driver_age' : self.passenger_info['driver_age'],
            'driver_numplate': self.passenger_info['driver_numplate']
        }
        self.accepted_passengers = requests.post(f"http://surveyer.pythonanywhere.com/passenger_accepted",json = self.accepted_passenger_info)
        print(self.accepted_passengers.content)
    
    #handling the driver declining
    def decline_incoming_passenger(self):
        return
        

#Creates an instance of the AcceptPassenger class
def accept_passenger(passenger_info):
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = AcceptPassenger(passenger_info)
        
    else:
        toplevel_window.focus()  # if window exists focus it
