import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

class ChatAPIClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat API Client")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)  # กำหนดขนาดขั้นต่ำ
        
        self.base_url = ""
        self.api_status = "Disconnected"
        self.selected_room = None
        self.token = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab 1: Connection
        connection_tab = ttk.Frame(self.notebook)
        self.notebook.add(connection_tab, text="Connection")
        
        # Tab 2: Authentication
        auth_tab = ttk.Frame(self.notebook)
        self.notebook.add(auth_tab, text="Authentication")
        
        # Tab 3: Chat
        chat_tab = ttk.Frame(self.notebook)
        self.notebook.add(chat_tab, text="Chat")
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, relief="sunken", anchor="w")
        status_label.pack(side="bottom", fill="x")
        
        # --- Connection Tab ---
        api_frame = ttk.LabelFrame(connection_tab, text="API Connection")
        api_frame.pack(padx=5, pady=5, fill="x")
        
        ttk.Label(api_frame, text="API URL:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.api_url_entry = ttk.Entry(api_frame, width=50)
        self.api_url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.api_url_entry.insert(0, "http://localhost:5555")
        
        ttk.Button(api_frame, text="Connect", command=self.connect_api).grid(row=0, column=2, padx=5, pady=5)
        
        status_frame = ttk.LabelFrame(connection_tab, text="API Status")
        status_frame.pack(padx=5, pady=5, fill="both", expand=True)
        
        self.api_status_var = tk.StringVar()
        self.api_status_var.set("Please connect to an API")
        ttk.Label(status_frame, textvariable=self.api_status_var, wraplength=700).pack(padx=5, pady=5, fill="both")
        
        ttk.Button(status_frame, text="Refresh Status", command=self.check_api_status).pack(pady=5)
        
        # --- Authentication Tab ---
        auth_frame = ttk.LabelFrame(auth_tab, text="Authentication")
        auth_frame.pack(padx=5, pady=5, fill="x")
        
        ttk.Label(auth_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(auth_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(auth_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(auth_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(auth_frame, text="Register", command=self.register).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(auth_frame, text="Login", command=self.login).grid(row=2, column=1, padx=5, pady=5)
        
        # --- Chat Tab ---
        # Room Management
        room_frame = ttk.LabelFrame(chat_tab, text="Room Management")
        room_frame.pack(padx=5, pady=5, fill="x")
        
        ttk.Label(room_frame, text="Room Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.room_name_entry = ttk.Entry(room_frame, width=30)
        self.room_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(room_frame, text="Create Room", command=self.create_room).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(room_frame, text="Refresh Rooms", command=self.refresh_rooms).grid(row=0, column=3, padx=5, pady=5)
        
        self.room_listbox = tk.Listbox(room_frame, height=8, width=50)
        self.room_listbox.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        self.room_listbox.bind('<<ListboxSelect>>', self.on_room_select)
        
        # Chat Display
        chat_frame = ttk.LabelFrame(chat_tab, text="Chat")
        chat_frame.pack(padx=5, pady=5, fill="both", expand=True)
        
        self.chat_display = tk.Text(chat_frame, height=15, state="disabled", wrap="word")
        self.chat_display.pack(padx=5, pady=5, fill="both", expand=True)
        
        message_frame = ttk.Frame(chat_frame)
        message_frame.pack(padx=5, pady=5, fill="x")
        
        self.message_entry = ttk.Entry(message_frame, width=60)
        self.message_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        ttk.Button(message_frame, text="Send", command=self.send_message).pack(side="right", padx=5)
        
        # Configure grid weights
        api_frame.columnconfigure(1, weight=1)
        room_frame.columnconfigure(1, weight=1)
        
    def connect_api(self):
        self.base_url = self.api_url_entry.get().strip()
        if not self.base_url:
            messagebox.showerror("Error", "Please enter an API URL!")
            return
        self.check_api_status()
        
    def check_api_status(self):
        if not self.base_url:
            self.api_status = "Disconnected"
            self.api_status_var.set("Please enter and connect to an API URL")
            self.status_var.set("API Status: Disconnected")
            return
            
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            print(f"API Check - Status: {response.status_code}, Response: {response.text}")
            if response.status_code == 200:
                self.api_status = "Connected"
                status_text = (
                    f"API Status: Connected\n"
                    f"Base URL: {self.base_url}\n"
                    f"Last Check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Response: {response.json().get('message')}"
                )
                self.refresh_rooms()
            else:
                self.api_status = "Disconnected"
                status_text = (
                    f"API Status: Disconnected\n"
                    f"Base URL: {self.base_url}\n"
                    f"Last Check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Response Code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            self.api_status = "Disconnected"
            status_text = (
                f"API Status: Disconnected\n"
                f"Base URL: {self.base_url}\n"
                f"Last Check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Error: {str(e)}"
            )
        
        self.api_status_var.set(status_text)
        self.status_var.set(f"API Status: {self.api_status}")
        
    def register(self):
        if self.api_status != "Connected":
            messagebox.showerror("Error", "API is not connected! Please connect first.")
            return
            
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
            
        print(f"Registering - Username: '{username}', Password: '{password}'")
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={"username": username, "password": password}
            )
            print(f"Register Response - Status: {response.status_code}, Content: {response.text}")
            if response.status_code == 200:
                self.status_var.set("Registration successful")
                messagebox.showinfo("Success", "Registered successfully! Please login.")
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
            else:
                self.status_var.set("Registration failed")
                messagebox.showerror("Error", f"Registration failed! Status: {response.status_code}\nResponse: {response.text}")
        except requests.exceptions.RequestException as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Connection error: {str(e)}")
            
    def login(self):
        if self.api_status != "Connected":
            messagebox.showerror("Error", "API is not connected! Please connect first.")
            return
            
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
            
        print(f"Logging in - Username: '{username}', Password: '{password}'")
        try:
            response = requests.post(
                f"{self.base_url}/auth/token",
                data={"username": username, "password": password},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            print(f"Login Response - Status: {response.status_code}, Content: {response.text}")
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.status_var.set("Login successful")
                messagebox.showinfo("Success", "Logged in successfully!")
                self.refresh_rooms()
                self.notebook.select(2)  # สลับไปที่แท็บ Chat หลังล็อกอิน
            else:
                self.status_var.set("Login failed")
                messagebox.showerror("Error", f"Login failed! Status: {response.status_code}\nResponse: {response.text}")
        except requests.exceptions.RequestException as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Connection error: {str(e)}")
            
    def create_room(self):
        if self.api_status != "Connected":
            messagebox.showerror("Error", "API is not connected! Please connect first.")
            return
            
        if not self.token:
            messagebox.showerror("Error", "Please login first!")
            return
            
        room_name = self.room_name_entry.get().strip()
        if not room_name:
            messagebox.showerror("Error", "Please enter a room name!")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            response = requests.post(
                f"{self.base_url}/chat/rooms",
                json={"name": room_name},
                headers=headers
            )
            print(f"Create Room Response - Status: {response.status_code}, Content: {response.text}")
            if response.status_code == 200:
                self.status_var.set("Room created")
                messagebox.showinfo("Success", "Room created successfully!")
                self.room_name_entry.delete(0, tk.END)
                self.refresh_rooms()
            else:
                self.status_var.set("Room creation failed")
                messagebox.showerror("Error", f"Failed to create room! Status: {response.status_code}\nResponse: {response.text}")
        except requests.exceptions.RequestException as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Connection error: {str(e)}")
            
    def refresh_rooms(self):
        if self.api_status != "Connected":
            return
            
        try:
            response = requests.get(f"{self.base_url}/chat/rooms")
            print(f"Get Rooms Response - Status: {response.status_code}, Content: {response.text}")
            if response.status_code == 200:
                rooms = response.json()
                self.room_listbox.delete(0, tk.END)
                for room in rooms:
                    self.room_listbox.insert(tk.END, f"{room['id']}: {room['name']}")
            else:
                print(f"Failed to fetch rooms - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching rooms: {str(e)}")
            
    def on_room_select(self, event):
        selection = self.room_listbox.curselection()
        if selection:
            room_text = self.room_listbox.get(selection[0])
            room_id = int(room_text.split(":")[0])
            self.selected_room = room_id
            self.status_var.set(f"Selected room: {room_text}")
            self.chat_display.config(state="normal")
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state="disabled")
            
    def send_message(self):
        if self.api_status != "Connected":
            messagebox.showerror("Error", "API is not connected! Please connect first.")
            return
            
        if not self.token:
            messagebox.showerror("Error", "Please login first!")
            return
            
        if not self.selected_room:
            messagebox.showerror("Error", "Please select a room first!")
            return
            
        message = self.message_entry.get().strip()
        if message:
            try:
                headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
                payload = {"content": message}
                print(f"Sending message - Headers: {headers}, Payload: {payload}")
                response = requests.post(
                    f"{self.base_url}/chat/rooms/{self.selected_room}/messages",
                    json=payload,
                    headers=headers
                )
                print(f"Send Message Response - Status: {response.status_code}, Content: {response.text}")
                if response.status_code == 200:
                    self.chat_display.config(state="normal")
                    self.chat_display.insert("end", f"You: {message}\n")
                    self.chat_display.insert("end", f"Response: Message sent\n\n")
                    self.chat_display.config(state="disabled")
                    self.message_entry.delete(0, tk.END)
                    self.status_var.set("Message sent")
                else:
                    self.status_var.set("Failed to send message")
                    messagebox.showerror("Error", f"Failed to send message! Status: {response.status_code}\nResponse: {response.text}")
            except requests.exceptions.RequestException as e:
                self.status_var.set(f"Error: {str(e)}")
                messagebox.showerror("Error", f"Connection error: {str(e)}")

def main():
    root = tk.Tk()
    app = ChatAPIClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()