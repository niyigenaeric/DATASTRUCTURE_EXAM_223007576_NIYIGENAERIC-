import tkinter as tk
from tkinter import ttk
import random
import string


# Utility Functions

def generate_taxi_id():
    """Generate a random alphanumeric Taxi ID with up to 5 characters."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# Car and Passenger Management

class Passenger:
    def __init__(self, passenger_number):
        self.passenger_number = passenger_number

class Taxi:
    def __init__(self, taxi_id, location, fare):
        self.taxi_id = taxi_id
        self.location = location
        self.fare = fare
        self.passengers = []
        self.capacity = 28  # Each taxi has a capacity of 28 passengers

    def assign_passenger(self, passenger):
        """Assign a passenger to this taxi if space is available."""
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            return True
        return False

    def available_slots(self):
        """Return the number of available slots for passengers."""
        return self.capacity - len(self.passengers)

    def is_full(self):
        """Check if the taxi is full."""
        return len(self.passengers) == self.capacity

class TaxiBookingSystem:
    def __init__(self):
        self.taxis = []
        # Removed booking history, not stored in memory anymore

    def add_taxi(self, location, fare):
        """Add a new taxi with a random Taxi ID to the system."""
        taxi_id = generate_taxi_id()
        taxi = Taxi(taxi_id, location, fare)
        self.taxis.append(taxi)

    def request_ride(self, passenger_number, taxi_id):
        """Request a ride for a passenger based on chosen Taxi ID."""
        passenger = Passenger(passenger_number)

        for taxi in self.taxis:
            if taxi.taxi_id == taxi_id:
                if not taxi.is_full():
                    if taxi.assign_passenger(passenger):
                        return taxi.taxi_id, taxi.location, taxi.fare  # Return taxi ID, location, and fare
                else:
                    return taxi.taxi_id, "Taxi is full", None
        return None, None, None

    def view_taxis(self):
        """View all taxis and their passenger counts."""
        taxi_info = []
        for taxi in self.taxis:
            slots_used = len(taxi.passengers)
            taxi_info.append((taxi.taxi_id, taxi.location, taxi.fare, slots_used, taxi.available_slots()))
        return taxi_info


# Tkinter GUI Implementation

class TaxiBookingApp:
    def __init__(self, root, system):
        self.root = root
        self.system = system

        # Configure full-screen mode
        self.root.attributes('-fullscreen', True)
        self.is_fullscreen = True
        self.root.configure(bg="#f0f0f0")

        # Custom control buttons
        self.control_frame = tk.Frame(self.root, bg="#34495e")
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.minimize_button = tk.Button(self.control_frame, text="Minimize", font=("Helvetica", 12), bg="#f39c12", fg="white", command=self.minimize_app)
        self.minimize_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.toggle_button = tk.Button(self.control_frame, text="Maximize", font=("Helvetica", 12), bg="#27ae60", fg="white", command=self.toggle_fullscreen)
        self.toggle_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.close_button = tk.Button(self.control_frame, text="Close", font=("Helvetica", 12), bg="#e74c3c", fg="white", command=self.close_app)
        self.close_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Stylish heading
        self.heading_label = tk.Label(self.root, text="Taxi Booking System", font=("Helvetica", 24, "bold"), fg="#2c3e50", bg="#f0f0f0")
        self.heading_label.pack(pady=20)

        # Passenger number entry
        self.passenger_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.passenger_frame.pack(pady=10)

        self.passenger_label = tk.Label(self.passenger_frame, text="Enter Your Phone Number:", font=("Helvetica", 14), bg="#f0f0f0")
        self.passenger_label.pack(side=tk.LEFT, padx=10)

        self.passenger_entry = tk.Entry(self.passenger_frame, font=("Helvetica", 14), bd=2, relief=tk.GROOVE)
        self.passenger_entry.pack(side=tk.LEFT, padx=10)

        # Filter by Taxi ID
        self.filter_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.filter_frame.pack(pady=10)

        self.filter_label = tk.Label(self.filter_frame, text="Filter by Taxi ID:", font=("Helvetica", 14), bg="#f0f0f0")
        self.filter_label.pack(side=tk.LEFT, padx=10)

        self.filter_entry = tk.Entry(self.filter_frame, font=("Helvetica", 14), bd=2, relief=tk.GROOVE)
        self.filter_entry.pack(side=tk.LEFT, padx=10)

        self.filter_button = tk.Button(self.filter_frame, text="Filter", font=("Helvetica", 14, "bold"), bg="#2980b9", fg="white", command=self.filter_by_taxi_id)
        self.filter_button.pack(side=tk.LEFT, padx=10)

        # Taxi display
        self.taxi_list_label = tk.Label(self.root, text="Available Taxis:", font=("Helvetica", 16), fg="#2980b9", bg="#f0f0f0")
        self.taxi_list_label.pack()

        self.taxi_tree = ttk.Treeview(self.root, columns=("Taxi ID", "Location", "Fare", "Passengers", "Available Slots"), show="headings", height=10)
        self.taxi_tree.heading("Taxi ID", text="Taxi ID")
        self.taxi_tree.heading("Location", text="Location")
        self.taxi_tree.heading("Fare", text="Fare (Frw)")
        self.taxi_tree.heading("Passengers", text="Passengers")
        self.taxi_tree.heading("Available Slots", text="Available Slots")
        self.taxi_tree.pack(pady=10)

        # Book Ride button
        self.book_ride_button = tk.Button(self.root, text="Book Ride", font=("Helvetica", 14, "bold"), bg="#2980b9", fg="white", command=self.book_ride, relief=tk.RAISED)
        self.book_ride_button.pack(pady=10)

        self.refresh_ui()

    def toggle_fullscreen(self):
        """Toggle between full-screen and windowed mode."""
        if self.is_fullscreen:
            self.root.attributes('-fullscreen', False)
            self.toggle_button.config(text="Maximize")
        else:
            self.root.attributes('-fullscreen', True)
            self.toggle_button.config(text="Restore")
        self.is_fullscreen = not self.is_fullscreen

    def minimize_app(self):
        """Minimize the application."""
        self.root.iconify()

    def close_app(self):
        """Close the application."""
        self.root.destroy()

    def filter_by_taxi_id(self):
        """Filter the taxis list based on Taxi ID."""
        taxi_id_filter = self.filter_entry.get().strip()
        taxis = self.system.view_taxis()

        filtered_taxis = [taxi for taxi in taxis if taxi_id_filter in taxi[0]]
        
        # Refresh the taxi list
        for row in self.taxi_tree.get_children():
            self.taxi_tree.delete(row)
        for taxi in filtered_taxis:
            self.taxi_tree.insert("", "end", values=taxi)

    def book_ride(self):
        """Book a ride and assign a taxi."""
        passenger_number = self.passenger_entry.get()
        selected_item = self.taxi_tree.selection()

        if not passenger_number or len(passenger_number) != 10 or not passenger_number.startswith(("078", "073", "072")):
            self.show_custom_popup("Invalid Phone Number", "Please enter a valid 10-digit phone number starting with 078, 073, or 072.", "error")
            return

        if selected_item:
            taxi_info = self.taxi_tree.item(selected_item)['values']
            taxi_id = taxi_info[0]

            taxi_id, location, fare = self.system.request_ride(passenger_number, taxi_id)
            if taxi_id:
                if fare is None:
                    self.show_custom_popup("Taxi Full", f"Sorry, Taxi {taxi_id} is full.", "warning")
                else:
                    self.show_custom_popup("Success", f"Ride booked successfully!\nPassenger assigned to Taxi: {taxi_id}\nLocation: {location}\nPrice: Frw {fare}\nPay with this number: *152*1*{taxi_id}#", "success")
            else:
                self.show_custom_popup("No Available Taxi", "Sorry, all taxis are full or taxi ID is not valid.", "warning")
        else:
            self.show_custom_popup("No Taxi Selected", "Please select a taxi from the list.", "warning")

        self.refresh_ui()

    def show_custom_popup(self, title, message, popup_type):
        """Display a custom popup window with a given title, message, and popup type (success, warning, error)."""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("400x200")
        popup.configure(bg="#ecf0f1")

        # Custom styling for different popup types
        if popup_type == "success":
            popup.config(bg="#2ecc71")  # Green for success
        elif popup_type == "warning":
            popup.config(bg="#f39c12")  # Yellow for warning
        elif popup_type == "error":
            popup.config(bg="#e74c3c")  # Red for error

        # Title label
        title_label = tk.Label(popup, text=title, font=("Helvetica", 16, "bold"), fg="white", bg=popup.cget("bg"))
        title_label.pack(pady=10)

        # Message label
        message_label = tk.Label(popup, text=message, font=("Helvetica", 12), fg="white", bg=popup.cget("bg"))
        message_label.pack(pady=10)

        # Close button
        close_button = tk.Button(popup, text="Close", font=("Helvetica", 14, "bold"), fg="white", bg="#34495e", command=popup.destroy, relief=tk.RAISED)
        close_button.pack(pady=20)

        popup.grab_set()  # Prevent interaction with the main window until this popup is closed

    def refresh_ui(self):
        """Refresh the lists of taxis in the GUI."""
        # Refresh taxi list
        for row in self.taxi_tree.get_children():
            self.taxi_tree.delete(row)
        taxis = self.system.view_taxis()
        for taxi in taxis:
            self.taxi_tree.insert("", "end", values=taxi)

# Main Execution

def main():
    system = TaxiBookingSystem()

    # Add some taxis with predefined locations and fares
    locations_with_fares = [
        ("Kigali-Huye", 3900),
        ("Kigali-Musanze", 3500),
        ("Kigali-Nyagatare", 4000),
        ("Kigali-Rusizi", 9000),
        ("Huye-Kigali", 3900),
        ("Musanze-Kigali", 3500),
        ("Nyagatare-Kigali", 4000),
        ("Rusizi-Kigali", 9000),
    ]
    for location, fare in locations_with_fares:
        system.add_taxi(location, fare)

    # Create the Tkinter window and app
    root = tk.Tk()
    app = TaxiBookingApp(root, system)

    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
