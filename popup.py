import customtkinter 
import requests
import json







class PickOthers(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.enter_name= customtkinter.CTkEntry(master=self,placeholder_text="Enter your name: ")
        self.enter_name.grid(row=0, column=0, sticky='nsew')

        self.enter_age = customtkinter.CTkEntry(master=self,placeholder_text="Enter your age: ")
        self.enter_age.grid(row=1, column=0, sticky='nsew')

        self.enter_numplate = customtkinter.CTkEntry(master=self,placeholder_text="Enter your car numberplate: ")
        self.enter_numplate.grid(row=2, column=0, sticky='nsew')

        self.start_search_button = customtkinter.CTkButton(master=self,text="Start Searching", command=self.wait_to_find_passenger)
        self.start_search_button.grid(row=3, column=0, sticky='nsew')
        
        self.grid_rowconfigure(0, weight=0)  # label row
        self.grid_rowconfigure(1, weight=1)  # enter_name row
        self.grid_rowconfigure(2, weight=1)  # enter_age row
        self.grid_rowconfigure(3, weight=1)  # enter_numplate row
        
    
        
    def wait_to_find_passenger(self):
        self.name = self.enter_name.get()
        self.age = self.enter_age.get()
        self.numplate = self.enter_numplate.get()
        
        
        if self.name != "" and self.numplate != "" and int(self.age) >= 17:
            self.data_to_send = {"name": self.name, "age": self.age, "numplate": self.numplate} 
            try:
                response = requests.post('http://surveyer.pythonanywhere.com/receive_data', json=self.data_to_send)
                response.raise_for_status()  # Raise an exception for HTTP errors
                response_data = response.json()
                print(response.status_code)
                print(response_data.get('name'),response_data.get('age'),response_data.get('numplate'))
            except requests.exceptions.RequestException as e:
                 print(f"Request error: {e}")

            


def PickUpOthers():
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = PickOthers()
    else:
        toplevel_window.focus()  # if window exists focus it
    
    

class GetPicked(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        
        self.enter_name= customtkinter.CTkEntry(master=self,placeholder_text="Enter your name: ")
        self.enter_name.grid(row=0, column=0, sticky='nsew')

        self.enter_age = customtkinter.CTkEntry(master=self,placeholder_text="Enter your age: ")
        self.enter_age.grid(row=1, column=0, sticky='nsew')

        self.start_search_button = customtkinter.CTkButton(master=self,text="Start Searching", command=self.wait_to_find_driver)
        self.start_search_button.grid(row=3, column=0, sticky='nsew')

        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_rowconfigure(2, weight=1)

    def wait_to_find_driver(self):
        self.name = self.enter_name.get()
        self.age = self.enter_age.get()
        
        if self.name != "" and self.age != "" and int(self.age) >= 13:
            self.data_to_send = {"name" : self.name, "age" : self.age}
            print("waiting to find driver")
            try:
                response = requests.post('http://surveyer.pythonanywhere.com/receive_data', json=self.data_to_send)
                response.raise_for_status()  # Raise an exception for HTTP errors
                response_data = response.json()
                print(response.status_code)
                print(response_data.get("name"),response_data.get("age"))
            except requests.exceptions.RequestException as e:
                 print(f"Request error: {e}")
        


        

def GetPickedUp(start_position,end_position):
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = GetPicked()  # create window if its None or destroyed
    else:
        toplevel_window.focus()  # if window exists focus it













