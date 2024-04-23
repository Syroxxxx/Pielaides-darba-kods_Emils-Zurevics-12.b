from tkinter import *
import sqlite3
import bcrypt
from tkinter import messagebox
from tkinter import ttk

connect = sqlite3.connect("fuelCalculator.db")
cursor = connect.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
   ''')
def connect_db():
  """Connects to the database and returns the connection object."""
  conn = sqlite3.connect("fuelCalculator.db")
  return conn

def drive_history():
    conn = connect_db()  
    cursor = conn.cursor()
    create_table = f"""
    CREATE TABLE IF NOT EXISTS {username} (
        user_id INTEGER PRIMARY KEY,
        nepieciesamais_tilpums INTEGER,
        izmaksas INTEGER,
        FOREIGN KEY(user_id) REFERENCES Users(id)
    )
    """
    
    query = f"""
  SELECT Users.user_id, Users.username, Users.password, 
         {username}.user_id, {username}.nepieciesamais_tilpums, {username}.izmaksas
  FROM Users
  JOIN {username} ON Users.user_id = {username}.user_id
  """
  
    cursor.execute(create_table)
            
    cursor = connect.execute(query)
            
    connect.commit()





choices = ["Benzīns 95", "Benzīns 98", "Dīzelis", "LPG"]

color = "gray"

class FuelCalculator:
    def __init__(self, distance, fuel_consumption):
        self.distance = distance
        self.fuel_consumption = fuel_consumption

    def calculate_fuel_volume(self):
        fuel_volume = self.distance * self.fuel_consumption / 100
        return fuel_volume



def calculator_Window(): 
    def calculate_fuel():
        global username
        distance = float(entry_distance.get().replace(',','.'))
        fuel_consumption = float(entry_fuel_consumption.get().replace(',','.'))
        gas_price = float(entry_gas_price.get().replace(',','.'))

        calculator = FuelCalculator(distance, fuel_consumption)
        fuel_volume = calculator.calculate_fuel_volume()
        rounded_fuel_volume = round(fuel_volume, 2)
        
        volume_needed = rounded_fuel_volume
        price_of_fill_up = volume_needed * gas_price
        rounded_price_of_fill_up = round(price_of_fill_up, 2)

        fuel_volume_needed["text"] = f"Nepieciešamais degvielas tilpums priekš brauciena ir {rounded_fuel_volume}L. \n {rounded_fuel_volume}L uzpilde maksās {rounded_price_of_fill_up}€"
        
        conn = connect_db()

        conn.execute(f"""INSERT INTO {username}(nepieciesamais_tilpums, izmaksas) VALUES (?, ?)""", (rounded_fuel_volume, rounded_price_of_fill_up))
        conn.commit()
        
        
   
        
        
    new_window = Tk()
    new_window.title("Degvielas kalkulators")
    new_window.geometry("400x400")
    new_window.config(bg = color)
    

    label_distance = Label(new_window, text="Distance (km):", bg = color)
    label_distance.pack()
    entry_distance = Entry(new_window)
    entry_distance.pack()

    label_fuel_consumption = Label(new_window, text="Degvielas patēriņš (l/100km):", bg = color)
    label_fuel_consumption.pack()
    entry_fuel_consumption = Entry(new_window)
    entry_fuel_consumption.pack()
    
    label_gas_price = Label(new_window, text = "Ievadi aktuālo auto degvielas cenu: ", bg = color)
    label_gas_price.pack()
    entry_gas_price = Entry(new_window)
    entry_gas_price.pack()
    
    label_gas_type = Label(new_window, text = "Izvēlies degvielas tipu", bg = color)
    label_gas_type.pack()
    choose = ttk.Combobox(new_window, values = choices)
    choose.pack()
    
    
    fuel_volume_needed = Label(new_window, text="", bg = color)
    fuel_volume_needed.pack()
    

    calculate_button = Button(new_window, text="Aprēķināt", width = 15, height = 1, command=calculate_fuel)
    calculate_button.pack()
    
    def go_back():
          new_window.destroy()
          menu_window()
          
    back_button = Button(new_window, text = "Atpakaļ", width = 15, height = 1, command = go_back)
    back_button.pack()

    new_window.mainloop()

def menu_window():
      menuWindow = Tk()
      menuWindow.title("Degvielas kalkulators")
      menuWindow.geometry("400x400")
      menuWindow.config(bg = color)
      
      def open_calculator_window():
            menuWindow.destroy()
            calculator_Window()
            
      def open_trip_history():
            print("hello")
      
      btn_fuel_volume = Button(menuWindow, text = "Degvielas tilpuma kalkulators", width = 22, height = 1, command = open_calculator_window)
      btn_fuel_volume.pack()
      
      btn_trip_history = Button(menuWindow, text = "Braucienu vēsture", width = 15, height = 1, command = open_trip_history)
      btn_trip_history.pack()
      
      menuWindow.mainloop()
      
def registerWindow():

    register_window = Tk()
    register_window.title("Reģistrēties")
    register_window.geometry("400x400")
    register_window.config(bg = color)

    label_newUsername = Label(register_window, text = "Lietotājvārds:", bg = color)
    label_newUsername.pack()
    entry_newUsername = Entry(register_window)
    entry_newUsername.pack()

    labelPassword = Label(register_window, text = "Parole:", bg = color)
    labelPassword.pack()
    entryPassword = Entry(register_window)
    entryPassword.pack()

    labelPasswordRepeat = Label(register_window, text = "Parole atkārtoti:", bg = color)
    labelPasswordRepeat.pack()
    entryPasswordRepeat = Entry(register_window)
    entryPasswordRepeat.pack()

    def openMenuWindow():
        global username
        username = entry_newUsername.get()
        password = entryPassword.get()
        password_repeat = entryPasswordRepeat.get()
        
        if not username or not password:
            messagebox.showerror("Degvielas kalkulators", "Trūkst lietotājvārds vai parole!")
            
        if password == password_repeat:
            connect = sqlite3.connect("FuelCalculator.db")
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            cursor = connect.cursor()
            data = "INSERT INTO users (username, password) VALUES (?, ?)"
            cursor.execute(data, (username, hashed_password))
            connect.commit()
        
            register_window.destroy()
            drive_history()
            menu_window()

        else:
            messagebox.showwarning("Degvielas kalkulators", "Paroles nesakrīt!")
    def goBack():
        register_window.destroy()
        startup_window()
        
    registerButton = Button(register_window, text = "Reģistrēties", width = 15, height = 1, command = openMenuWindow)
    registerButton.pack()

    backButton = Button(register_window, text = "Atpakaļ", width = 15, height = 1, command = goBack)
    backButton.pack()

def check_credentials(username, password):
    connect = sqlite3.connect("fuelCalculator.db")
    cursor = connect.cursor()
    
    data = "SELECT password FROM Users WHERE username = ?"
    cursor.execute(data, (username,))
    
    hashed_password = cursor.fetchone()
    
    if hashed_password:
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password[0]):
            login_window.destroy()
            menu_window()
        else:
            messagebox.showwarning("Fuel Calculator", "Nepareiza parole")
    else:
        messagebox.showwarning("Fuel Calculator", "Lietotājvārds netika atrasts")
    
def loginWindow():
    global login_window, entry_username, entry_password
    login_window = Tk()
    login_window.title("Ielogoties")
    login_window.geometry("400x400")
    login_window.config(bg = color)
    login_window.protocol("WM_DELETE_WINDOW")

    label_username = Label(login_window, text = "Lietotājvārds:", bg = color)
    label_username.pack()
    entry_username = Entry(login_window)
    entry_username.pack()

    label_password = Label(login_window, text="Parole:", bg = color)
    label_password.pack()
    entry_password = Entry(login_window, show="*")
    entry_password.pack()

    error_label = Label(login_window, text="", bg = color)
    error_label.pack()

    def loginButtonClicked():
        username = entry_username.get()
        password = entry_password.get()
        connect_db()
        check_credentials(username, password)
    
    login_button = Button(login_window, text="Ielogoties", width = 15, height = 1, command=loginButtonClicked)
    login_button.pack()

    login_window.mainloop()

def startup_window():
        def LoginPressed():
            startupWindow.destroy()
            loginWindow()

        def RegisterPressed():
            startupWindow.destroy()
            registerWindow()

        startupWindow = Tk()
        startupWindow.title("Degvielas kalkulātors")
        startupWindow.geometry("400x400")
        startupWindow.config(bg = color)
        

        toLoginButton = Button(startupWindow, text = "Ielogototies", width = 15, height = 1, command = LoginPressed)
        toLoginButton.pack()

        toRegisterButton = Button(startupWindow, text = "Reģistrēties", width = 15, height = 1, command = RegisterPressed)
        toRegisterButton.pack()
        
        startupWindow.mainloop()
        
startup_window()
