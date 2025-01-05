import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Class representing each ride with a priority score
class TaxiBookingSystem:
    def __init__(self):
        self.rides = []  # Store rides with a priority score

    def add_ride(self, ride_id, ride_data, priority_score):
        """
        Add a ride with a priority score to the system.
        """
        ride = {"ride_id": ride_id, "ride_data": ride_data, "priority_score": priority_score}
        self.rides.append(ride)

    def bucket_sort(self):
        """
        Sort the rides based on the priority score using Bucket Sort.
        """
        if len(self.rides) == 0:
            return  # No rides to sort
        
        # Find the maximum and minimum priority scores to determine the range
        max_score = max(self.rides, key=lambda ride: ride["priority_score"])["priority_score"]
        min_score = min(self.rides, key=lambda ride: ride["priority_score"])["priority_score"]

        if max_score == min_score:
            return  # No sorting needed if all priority scores are the same

        # Define the number of buckets
        bucket_count = len(self.rides)

        # Create empty buckets
        buckets = [[] for _ in range(bucket_count)]

        # Map each ride to a bucket based on its priority score
        for ride in self.rides:
            # Scale the priority score to map it to a bucket
            bucket_index = int((ride["priority_score"] - min_score) / (max_score - min_score) * (bucket_count - 1))
            buckets[bucket_index].append(ride)

        # Sort each bucket and concatenate them back
        sorted_rides = []
        for bucket in buckets:
            sorted_rides.extend(sorted(bucket, key=lambda ride: ride["priority_score"]))

        self.rides = sorted_rides

    def display_rides(self):
        """
        Return the rides for display.
        """
        return self.rides


class FlashyPopup:
    def __init__(self, parent, message, title="Notification"):
        self.popup = tk.Toplevel(parent)
        self.popup.geometry("300x150")
        self.popup.title(title)
        self.popup.config(bg="#f39c12")
        self.popup.attributes("-topmost", True)
        self.popup.resizable(False, False)

        label = tk.Label(self.popup, text=message, font=("Helvetica", 14, "bold"), bg="#f39c12", fg="white")
        label.pack(expand=True)

        close_button = tk.Button(self.popup, text="Close", command=self.popup.destroy, font=("Arial", 12), bg="#e74c3c", fg="white")
        close_button.pack(side="bottom", pady=10)

        # Make the popup 'flash' (add an animation)
        self.flash_popup()

    def flash_popup(self):
        """Creates a flashing effect for the pop-up."""
        color_cycle = ["#e74c3c", "#f39c12", "#2ecc71"]
        self._cycle_color(color_cycle)

    def _cycle_color(self, color_cycle):
        """Cycle through colors for the flashing effect."""
        def change_color(index=0):
            if index < len(color_cycle):
                self.popup.config(bg=color_cycle[index])
                index += 1
                self.popup.after(500, change_color, index)  # Change color every 500ms
            else:
                self.popup.config(bg=color_cycle[0])  # Reset to starting color

        change_color()


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

        # Minimize button
        self.minimize_button = tk.Button(self.control_frame, text="Minimize", font=("Helvetica", 12), bg="#f39c12", fg="white", command=self.minimize_app)
        self.minimize_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Maximize/Restore button
        self.toggle_button = tk.Button(self.control_frame, text="Maximize", font=("Helvetica", 12), bg="#27ae60", fg="white", command=self.toggle_fullscreen)
        self.toggle_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Close button
        self.close_button = tk.Button(self.control_frame, text="Close", font=("Helvetica", 12), bg="#e74c3c", fg="white", command=self.close_app)
        self.close_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Stylish heading
        self.heading_label = tk.Label(self.root, text="Taxi Booking System", font=("Helvetica", 24, "bold"), fg="#2c3e50", bg="#f0f0f0")
        self.heading_label.pack(pady=20)

        # Treeview widget to display rides
        self.tree_view = ttk.Treeview(root, show="tree headings")
        self.tree_view["columns"] = ("Ride Data", "Priority Score")
        self.tree_view.heading("#0", text="Ride ID", anchor="w")
        self.tree_view.heading("Ride Data", text="Ride Data", anchor="w")
        self.tree_view.heading("Priority Score", text="Priority Score", anchor="w")
        self.tree_view.column("#0", stretch=tk.YES, width=150)
        self.tree_view.column("Ride Data", stretch=tk.YES, width=350)
        self.tree_view.column("Priority Score", stretch=tk.YES, width=150)
        self.tree_view.pack(expand=True, fill="both", pady=10, padx=10)

        # Create controls for adding rides and sorting
        self.create_controls()

    def minimize_app(self):
        """
        Minimize the application.
        """
        self.root.iconify()

    def toggle_fullscreen(self):
        """
        Toggle between full-screen and windowed mode.
        """
        if self.is_fullscreen:
            self.root.state('normal')  # Restore windowed mode
            self.toggle_button.config(text="Maximize")
        else:
            self.root.attributes('-fullscreen', True)  # Full-screen mode
            self.toggle_button.config(text="Restore")
        self.is_fullscreen = not self.is_fullscreen

    def close_app(self):
        """
        Close the application.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()

    def create_controls(self):
        """
        Creates input fields and buttons for adding rides and sorting.
        """
        controls_frame = tk.Frame(self.root, bg="#d9e4ea", bd=2, relief="ridge")
        controls_frame.pack(pady=10, padx=10, fill="x")

        # Ride ID input
        tk.Label(controls_frame, text="Ride ID:", bg="#d9e4ea", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ride_id_entry = tk.Entry(controls_frame, font=("Arial", 12), width=25)
        self.ride_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Ride Data input
        tk.Label(controls_frame, text="Ride Data (e.g., Pick-up location, Drop-off):", bg="#d9e4ea", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ride_data_entry = tk.Entry(controls_frame, font=("Arial", 12), width=25)
        self.ride_data_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Priority Score input
        tk.Label(controls_frame, text="Priority Score (1-10):", bg="#d9e4ea", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.priority_score_entry = tk.Entry(controls_frame, font=("Arial", 12), width=25)
        self.priority_score_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Buttons
        tk.Button(controls_frame, text="Add Ride", command=self.add_ride, font=("Arial", 12), bg="#5bc0de", fg="white", padx=10).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(controls_frame, text="Sort Rides", command=self.sort_rides, font=("Arial", 12), bg="#f39c12", fg="white", padx=10).grid(row=1, column=2, padx=10, pady=5)

    def add_ride(self):
        """
        Add a new ride with a priority score to the system.
        """
        ride_id = self.ride_id_entry.get()
        ride_data = self.ride_data_entry.get()
        try:
            priority_score = float(self.priority_score_entry.get())
        except ValueError:
            FlashyPopup(self.root, "Priority Score must be a number.", title="Error")
            return

        if ride_id and ride_data and priority_score:
            self.system.add_ride(ride_id, ride_data, priority_score)
            self.update_tree_view()
            FlashyPopup(self.root, f"Ride '{ride_id}' added successfully!", title="Success")
        else:
            FlashyPopup(self.root, "Please fill all fields.", title="Error")

    def sort_rides(self):
        """
        Sort the rides based on the priority score using Bucket Sort.
        """
        self.system.bucket_sort()
        self.update_tree_view()

    def update_tree_view(self):
        """
        Update the Treeview with the sorted rides.
        """
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        for ride in self.system.display_rides():
            self.tree_view.insert("", "end", text=ride["ride_id"], values=(ride["ride_data"], ride["priority_score"]))


# Run the application
if __name__ == "__main__":
    system = TaxiBookingSystem()
    root = tk.Tk()
    app = TaxiBookingApp(root, system)
    root.mainloop()
