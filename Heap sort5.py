import tkinter as tk
from tkinter import ttk
import heapq


class RideShareHeap:
    def __init__(self):
        # Reverse the priority_map so that 'emergency' has the highest priority number
        self.heap = []  # Min-heap to store bookings
        self.priority_map = {"low": 4, "medium": 3, "high": 2, "emergency": 5}  # emergency -> 5
        self.booking_counter = 0  # Unique counter to avoid conflicts in priority

    def add_booking(self, phone_number, priority_level, start, destination):
        self.booking_counter += 1
        priority = self.priority_map[priority_level]
        booking = (priority, self.booking_counter, phone_number, start, destination)
        heapq.heappush(self.heap, booking)
        return f"Booking added: Phone={phone_number}, Priority={priority_level}, Route={start} → {destination}"

    def serve_booking(self):
        if self.heap:
            priority, counter, phone_number, start, destination = heapq.heappop(self.heap)
            return f"Serving booking: Phone={phone_number}, Priority={priority}, Route={start} → {destination}"
        else:
            return "No bookings to serve."

    def view_bookings(self, destination_filter=None):
        if destination_filter:
            filtered_bookings = [
                (b[2], b[0], b[3], b[4])
                for b in self.heap
                if b[4] == destination_filter
            ]
        else:
            filtered_bookings = [(b[2], b[0], b[3], b[4]) for b in self.heap]

        # Sort by priority (with higher values now being lower priority) and booking counter
        sorted_bookings = sorted(filtered_bookings, key=lambda x: (x[1], x[0]))
        return sorted_bookings


class RideShareApp:
    def __init__(self, root):
        self.system = RideShareHeap()
        self.root = root
        self.root.title("Ride Sharing Taxi Booking System")
        self.root.state("zoomed")  # Maximize the window at startup
        self.root.configure(bg="#f0f0f0")

        # Heading
        heading_label = tk.Label(
            self.root, text="Ride Sharing Taxi Booking System", font=("Helvetica", 18, "bold"), bg="#f0f0f0"
        )
        heading_label.pack(pady=10)

        # Add Booking Frame
        add_frame = tk.Frame(self.root, bg="#f0f0f0")
        add_frame.pack(pady=20)

        tk.Label(add_frame, text="Phone Number:", font=("Helvetica", 12), bg="#f0f0f0").grid(
            row=0, column=0, padx=10, pady=5, sticky="e"
        )
        self.phone_entry = tk.Entry(add_frame, font=("Helvetica", 12))
        self.phone_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_frame, text="Priority Level:", font=("Helvetica", 12), bg="#f0f0f0").grid(
            row=0, column=2, padx=10, pady=5, sticky="e"
        )
        self.priority_var = tk.StringVar(value="low")
        priority_menu = ttk.Combobox(
            add_frame,
            textvariable=self.priority_var,
            values=["low", "medium", "high", "emergency"],
            state="readonly",
            font=("Helvetica", 12),
        )
        priority_menu.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(add_frame, text="Starting Location:", font=("Helvetica", 12), bg="#f0f0f0").grid(
            row=1, column=0, padx=10, pady=5, sticky="e"
        )
        self.start_var = tk.StringVar(value="Kigali")
        start_menu = ttk.Combobox(
            add_frame, textvariable=self.start_var, values=["Kigali"], state="readonly", font=("Helvetica", 12)
        )
        start_menu.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(add_frame, text="Destination:", font=("Helvetica", 12), bg="#f0f0f0").grid(
            row=1, column=2, padx=10, pady=5, sticky="e"
        )
        self.dest_var = tk.StringVar(value="Huye")
        dest_menu = ttk.Combobox(
            add_frame,
            textvariable=self.dest_var,
            values=["Huye", "Musanze", "Nyagatare", "Rusizi"],
            state="readonly",
            font=("Helvetica", 12),
        )
        dest_menu.grid(row=1, column=3, padx=10, pady=5)

        add_button = tk.Button(
            add_frame,
            text="Add Booking",
            font=("Helvetica", 12),
            bg="#27ae60",
            fg="white",
            command=self.add_booking,
        )
        add_button.grid(row=1, column=4, padx=20, pady=5)

        # Filter and Serve Buttons
        filter_frame = tk.Frame(self.root, bg="#f0f0f0")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter by Destination:", font=("Helvetica", 12), bg="#f0f0f0").grid(
            row=0, column=0, padx=10, pady=5, sticky="e"
        )
        self.filter_var = tk.StringVar(value="All")
        filter_menu = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "Huye", "Musanze", "Nyagatare", "Rusizi"],
            state="readonly",
            font=("Helvetica", 12),
        )
        filter_menu.grid(row=0, column=1, padx=10, pady=5)

        filter_button = tk.Button(
            filter_frame,
            text="Apply Filter",
            font=("Helvetica", 12),
            bg="#3498db",
            fg="white",
            command=self.apply_filter,
        )
        filter_button.grid(row=0, column=2, padx=20, pady=5)

        serve_button = tk.Button(
            filter_frame,
            text="Serve Booking",
            font=("Helvetica", 12),
            bg="#e74c3c",
            fg="white",
            command=self.serve_booking,
        )
        serve_button.grid(row=0, column=3, padx=20, pady=5)

        # Bookings List
        self.tree = ttk.Treeview(
            self.root, columns=("Phone Number", "Priority", "Start", "Destination"), show="headings", height=15
        )
        self.tree.heading("Phone Number", text="Phone Number")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Start", text="Start")
        self.tree.heading("Destination", text="Destination")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Status Label
        self.status_label = tk.Label(
            self.root, text="", font=("Helvetica", 12), fg="green", bg="#f0f0f0"
        )
        self.status_label.pack(pady=10)

        self.refresh_bookings()

    def add_booking(self):
        phone = self.phone_entry.get()
        priority = self.priority_var.get()
        start = self.start_var.get()
        destination = self.dest_var.get()

        if not phone or not priority:
            self.status_label.config(text="Error: Phone and Priority fields are required.", fg="red")
            return

        if start == destination:
            self.status_label.config(text="Error: Start and Destination cannot be the same.", fg="red")
            return

        if not self.validate_phone(phone):
            self.status_label.config(
                text="Error: Phone must have 10 digits and start with 078, 079, 072, or 073.", fg="red"
            )
            return

        message = self.system.add_booking(phone, priority, start, destination)
        self.status_label.config(text=message, fg="green")
        self.phone_entry.delete(0, tk.END)
        self.refresh_bookings()

    def validate_phone(self, phone):
        """
        Validate phone number format: must have 10 digits and start with 078, 079, 072, or 073.
        """
        return phone.isdigit() and len(phone) == 10 and phone[:3] in {"078", "079", "072", "073"}

    def serve_booking(self):
        message = self.system.serve_booking()
        self.status_label.config(text=message, fg="green" if "Serving" in message else "red")
        self.refresh_bookings()

    def apply_filter(self):
        destination = self.filter_var.get()
        if destination == "All":
            self.refresh_bookings()
        else:
            self.refresh_bookings(destination_filter=destination)

    def refresh_bookings(self, destination_filter=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        bookings = self.system.view_bookings(destination_filter=destination_filter)
        for booking in bookings:
            self.tree.insert("", "end", values=booking)


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = RideShareApp(root)
    root.mainloop()
