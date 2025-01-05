import tkinter as tk
from tkinter import ttk, messagebox
import random
import re

# Utility Functions
def generate_taxi_id(destination):
    """Generate a unique Taxi ID based on the destination."""
    return f"TAXI-{destination[:3].upper()}-{random.randint(1000, 9999)}"

# Car and Passenger Management
class Passenger:
    def __init__(self, passenger_number, start_location, destination):
        self.passenger_number = passenger_number
        self.start_location = start_location
        self.destination = destination

class Taxi:
    def __init__(self, taxi_id, location, fare):
        self.taxi_id = taxi_id
        self.location = location
        self.fare = fare
        self.passengers = []
        self.capacity = 5  # Set the capacity to 5 passengers

    def assign_passenger(self, passenger):
        """Assign a passenger to the taxi if there is space."""
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            return True
        return False

    def available_slots(self):
        """Returns the available slots in the taxi."""
        return self.capacity - len(self.passengers)

class TaxiBookingSystem:
    def __init__(self):
        self.taxis = []
        self.booking_history = []
        self.routes = {
            "Kigali-Huye": 3900,
            "Kigali-Musanze": 3500,
            "Kigali-Nyagatare": 4000,
            "Kigali-Rusizi": 9000
        }

    def add_taxi(self, destination, fare):
        taxi_id = generate_taxi_id(destination)
        taxi = Taxi(taxi_id, destination, fare)
        self.taxis.append(taxi)

    def request_ride(self, passenger_number, start_location, destination):
        passenger = Passenger(passenger_number, start_location, destination)

        route_key = f"{start_location}-{destination}"
        if route_key not in self.routes:
            return None, "Invalid route selected", None

        fare = self.routes[route_key]
        for taxi in self.taxis:
            if taxi.location == destination and taxi.assign_passenger(passenger):
                self.booking_history.append((passenger_number, taxi.taxi_id, destination, fare, start_location, destination))
                return taxi.taxi_id, destination, fare

        return None, "No available taxis", None

    def get_booking_history(self, destination_filter=None):
        if destination_filter:
            return [record for record in self.booking_history if record[5] == destination_filter]
        return self.booking_history

    def clear_booking_history(self):
        self.booking_history = []

# Tkinter GUI Implementation
class TaxiBookingApp:
    def __init__(self, root, system):
        self.root = root
        self.system = system

        # Set window title and size
        self.root.title("Taxi Booking System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")

        # Create main frame with padding
        main_frame = tk.Frame(self.root, padx=10, pady=10, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Heading with clear formatting
        heading_label = tk.Label(main_frame, text="Taxi Booking System", font=("Helvetica", 24, "bold"), pady=20, bg="#004d99", fg="white")
        heading_label.pack(fill=tk.X)

        # Booking Section Frame
        booking_frame = tk.Frame(main_frame, bg="#f5f5f5")
        booking_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Booking Section Labels and Entries
        tk.Label(booking_frame, text="Phone Number:", font=("Helvetica", 12), bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.phone_entry = tk.Entry(booking_frame, width=20, font=("Helvetica", 12))
        self.phone_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(booking_frame, text="Start Location:", font=("Helvetica", 12), bg="#f5f5f5").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.start_location_combobox = ttk.Combobox(booking_frame, values=["Kigali"], state="readonly", width=20, font=("Helvetica", 12))
        self.start_location_combobox.set("Kigali")
        self.start_location_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(booking_frame, text="Destination:", font=("Helvetica", 12), bg="#f5f5f5").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.destination_combobox = ttk.Combobox(booking_frame, values=["Huye", "Musanze", "Nyagatare", "Rusizi"], state="readonly", width=20, font=("Helvetica", 12))
        self.destination_combobox.set("Huye")
        self.destination_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Book Ride Button
        book_ride_button = tk.Button(booking_frame, text="Book Ride", command=self.book_ride, width=20, bg="#007acc", fg="white", font=("Helvetica", 12, "bold"))
        book_ride_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Booking History Section Frame
        history_frame = tk.Frame(main_frame, bg="#f5f5f5")
        history_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Booking History Heading
        history_heading_label = tk.Label(history_frame, text="Booking History", font=("Helvetica", 14, "bold"), bg="#f5f5f5")
        history_heading_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="w")

        # History Filter
        self.filter_combobox = ttk.Combobox(history_frame, values=["All", "Huye", "Musanze", "Nyagatare", "Rusizi"], state="readonly", width=20, font=("Helvetica", 12))
        self.filter_combobox.set("All")
        self.filter_combobox.grid(row=1, column=0, padx=5, pady=5)
        filter_button = tk.Button(history_frame, text="Filter", command=self.filter_history, width=10, bg="#28a745", fg="white", font=("Helvetica", 12))
        filter_button.grid(row=1, column=1, padx=5, pady=5)
        clear_history_button = tk.Button(history_frame, text="Clear History", command=self.clear_history, width=15, bg="#dc3545", fg="white", font=("Helvetica", 12))
        clear_history_button.grid(row=1, column=2, padx=5, pady=5)

        # History Table
        self.history_tree = ttk.Treeview(history_frame, columns=("Phone", "Taxi ID", "Destination", "Fare", "Start", "End"), show="headings")
        for col in ["Phone", "Taxi ID", "Destination", "Fare", "Start", "End"]:
            self.history_tree.heading(col, text=col)
        self.history_tree.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Make history_tree expandable
        history_frame.rowconfigure(2, weight=1)
        history_frame.columnconfigure(0, weight=1)

        self.refresh_history()

    def validate_phone(self):
        phone_number = self.phone_entry.get()
        if re.match(r"^(078|079|072|073)\d{7}$", phone_number):
            return True
        else:
            return False

    def book_ride(self):
        passenger_number = self.phone_entry.get()
        start_location = self.start_location_combobox.get()
        destination = self.destination_combobox.get()

        if not passenger_number or len(passenger_number) != 10 or not passenger_number.isdigit():
            messagebox.showerror("Error", "Please enter a valid phone number.")
            return

        if start_location == destination:
            messagebox.showerror("Error", "Start and destination cannot be the same. Please select different locations.")
            return

        result = messagebox.askyesno("Confirm Booking", f"Are you sure you want to book the ride to {destination}?")
        if result:
            taxi_id, location, fare = self.system.request_ride(passenger_number, start_location, destination)
            if taxi_id:
                messagebox.showinfo("Success!", f"Your ride is booked!\nTaxi ID: {taxi_id}\nFare: {fare} RWF\nDestination: {location}")
            else:
                messagebox.showerror("No Available Taxis", location)
            self.refresh_history()

    def refresh_history(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        for record in self.system.get_booking_history():
            self.history_tree.insert("", tk.END, values=record)

    def filter_history(self):
        filter_value = self.filter_combobox.get()
        if filter_value == "All":
            filtered = self.system.get_booking_history()
        else:
            filtered = self.system.get_booking_history(destination_filter=filter_value)

        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        for record in filtered:
            self.history_tree.insert("", tk.END, values=record)

    def clear_history(self):
        result = messagebox.askyesno("Clear History", "Are you sure you want to clear all booking history? This action cannot be undone.")
        if result:
            self.system.clear_booking_history()
            self.refresh_history()

    def on_close(self):
        result = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if result:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    system = TaxiBookingSystem()
    system.add_taxi("Huye", 3900)
    system.add_taxi("Musanze", 3500)
    system.add_taxi("Nyagatare", 4000)
    system.add_taxi("Rusizi", 9000)
    app = TaxiBookingApp(root, system)
    
    # Set the on_close method to handle window close event
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    
    root.state("zoomed")
    root.mainloop()
