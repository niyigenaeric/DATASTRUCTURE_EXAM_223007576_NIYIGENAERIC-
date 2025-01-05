import tkinter as tk
from tkinter import ttk
import random
import string

# ==============================
# Utility Functions
# ==============================
def generate_taxi_id():
    """Generate a random alphanumeric Taxi ID with up to 5 characters."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# ==============================
# Car and Passenger Management
# ==============================
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
        self.booking_history = []  # Store booking history

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
                        # Log the booking history
                        self.booking_history.append((passenger_number, taxi_id, taxi.location, taxi.fare))
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

    def get_booking_history(self):
        """Retrieve booking history."""
        return self.booking_history

# ==============================
# Tkinter GUI Implementation
# ==============================
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

        # Book Ride form
        self.book_ride_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.book_ride_frame.pack(pady=10)

        self.phone_label = tk.Label(self.book_ride_frame, text="Phone Number:", font=("Helvetica", 14), bg="#f0f0f0")
        self.phone_label.pack(side=tk.LEFT, padx=10)

        self.phone_entry = tk.Entry(self.book_ride_frame, font=("Helvetica", 14), bd=2, relief=tk.GROOVE)
        self.phone_entry.pack(side=tk.LEFT, padx=10)

        self.book_ride_button = tk.Button(self.book_ride_frame, text="Book Ride", font=("Helvetica", 14, "bold"), bg="#2980b9", fg="white", command=self.book_ride, relief=tk.RAISED)
        self.book_ride_button.pack(side=tk.LEFT, padx=10)

        # Booking history section with scroll
        self.history_label = tk.Label(self.root, text="Booking History:", font=("Helvetica", 16), fg="#16a085", bg="#f0f0f0")
        self.history_label.pack(pady=10)

        # Create a frame to hold the Treeview and Scrollbar
        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(pady=10)

        # Add the Scrollbar
        self.history_scrollbar = tk.Scrollbar(self.history_frame, orient="vertical")

        # Create Treeview for booking history
        self.history_tree = ttk.Treeview(self.history_frame, columns=("Phone Number", "Taxi ID", "Location", "Fare"), show="headings", height=5, yscrollcommand=self.history_scrollbar.set)
        self.history_tree.heading("Phone Number", text="Phone Number")
        self.history_tree.heading("Taxi ID", text="Taxi ID")
        self.history_tree.heading("Location", text="Location")
        self.history_tree.heading("Fare", text="Fare (Frw)")
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Attach the scrollbar to the Treeview
        self.history_scrollbar.config(command=self.history_tree.yview)
        self.history_scrollbar.pack(side=tk.RIGHT, fill="y")

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
        """Show a confirmation popup before closing the application."""
        confirmation_popup = tk.Toplevel(self.root)
        confirmation_popup.title("Confirm Close")
        confirmation_popup.geometry("300x150")
        confirmation_popup.configure(bg="#ecf0f1")

        # Title label
        title_label = tk.Label(confirmation_popup, text="Do you want to quit?", font=("Helvetica", 14, "bold"), fg="black", bg="#ecf0f1")
        title_label.pack(pady=20)

        # Yes button
        yes_button = tk.Button(confirmation_popup, text="Yes", font=("Helvetica", 12), fg="white", bg="#e74c3c", command=self.quit_app)
        yes_button.pack(side=tk.LEFT, padx=30, pady=10)

        # No button
        no_button = tk.Button(confirmation_popup, text="No", font=("Helvetica", 12), fg="white", bg="#27ae60", command=confirmation_popup.destroy)
        no_button.pack(side=tk.RIGHT, padx=30, pady=10)

        confirmation_popup.grab_set()  # Prevent interaction with the main window until this popup is closed

    def quit_app(self):
        """Close the application."""
        self.root.destroy()

    def book_ride(self):
        """Book a ride and assign a taxi."""
        passenger_number = self.phone_entry.get()
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

        # Refresh booking history
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        history = self.system.get_booking_history()
        for record in history:
            self.history_tree.insert("", "end", values=record)

# ==============================
# Main Execution
# ==============================
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

    root = tk.Tk()
    app = TaxiBookingApp(root, system)
    root.mainloop()

main()
