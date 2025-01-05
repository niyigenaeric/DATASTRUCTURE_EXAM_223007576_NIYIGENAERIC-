import tkinter as tk
from tkinter import ttk, messagebox

class TreeNode:
    def __init__(self, node_id, data):
        self.node_id = node_id
        self.data = data
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

class CustomMessageBox:
    def __init__(self, parent, message, title="Message", button_text="OK"):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("300x150")
        self.top.config(bg="#f8f9fa")
        self.top.resizable(False, False)

        # Custom Close, Minimize, Maximize Behavior (Optional)
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

        # Message Label
        message_label = tk.Label(self.top, text=message, font=("Arial", 14), bg="#f8f9fa", fg="#495057")
        message_label.pack(pady=20)

        # Button to close the message box
        close_button = tk.Button(self.top, text=button_text, font=("Arial", 12), bg="#5bc0de", fg="white", command=self.top.destroy)
        close_button.pack(pady=10)

    def on_close(self):
        self.top.destroy()

class TaxiBookingSystem:
    def __init__(self):
        self.root = TreeNode("root", {"type": "system", "description": "Taxi Booking System Root"})

    def add_ride(self, region_id, ride_id, ride_data):
        region_node = self.find_node(self.root, region_id)
        if region_node:
            ride_node = TreeNode(f"ride_{ride_id}", {"type": "ride", "data": ride_data})
            region_node.add_child(ride_node)
            return True
        return False

    def find_node(self, current_node, target_id):
        if current_node.node_id == target_id:
            return current_node
        for child in current_node.children:
            result = self.find_node(child, target_id)
            if result:
                return result
        return None

    def display_tree(self, node, tree_view, parent=""):
        data_display = f"Type: {node.data.get('type', 'N/A')}, Data: {node.data.get('description', node.data.get('data', 'N/A'))}"
        node_id = tree_view.insert(parent, "end", text=f"{node.node_id}", values=[data_display])
        for child in node.children:
            self.display_tree(child, tree_view, node_id)

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

        # Create Treeview widget
        self.tree_view = ttk.Treeview(root, show="tree headings")
        self.tree_view["columns"] = ("Data",)
        self.tree_view.heading("#0", text="Node ID", anchor="w")
        self.tree_view.heading("Data", text="Data", anchor="w")
        self.tree_view.column("#0", stretch=tk.YES, width=200)
        self.tree_view.column("Data", stretch=tk.YES, width=400)
        self.tree_view.pack(expand=True, fill="both", pady=10, padx=10)

        # Add controls for adding regions and rides
        self.create_controls()

    def create_controls(self):
        """
        Creates input fields and buttons for adding nodes.
        """
        controls_frame = tk.Frame(self.root, bg="#d9e4ea", bd=2, relief="ridge")
        controls_frame.pack(pady=10, padx=10, fill="x")

        # Region input
        tk.Label(controls_frame, text="Region Name/ID:", bg="#d9e4ea", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.region_id_entry = ttk.Combobox(controls_frame, font=("Arial", 12), width=25, values=[
            "Kigali-Huye", "Kigali-Musanze", "Kigali-Nyagatare", "Kigali-Rusizi",
            "Huye-Kigali", "Musanze-Kigali", "Rusizi-Kigali", "Nyagatare-Kigali"
        ], state="readonly")  # Make combobox readonly
        self.region_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Ride input
        tk.Label(controls_frame, text="Ride ID:", bg="#d9e4ea", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ride_id_entry = ttk.Combobox(controls_frame, font=("Arial", 12), width=25, state="readonly")  # Make combobox readonly
        self.ride_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.region_id_entry.bind("<<ComboboxSelected>>", self.update_ride_options)

        tk.Label(controls_frame, text="Ride Data:", bg="#d9e4ea", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ride_data_entry = tk.Entry(controls_frame, font=("Arial", 12), width=25)
        self.ride_data_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Buttons
        tk.Button(controls_frame, text="Add Region", command=self.add_region, font=("Arial", 12), bg="#5bc0de", fg="white", padx=10).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(controls_frame, text="Add Ride", command=self.add_ride, font=("Arial", 12), bg="#5cb85c", fg="white", padx=10).grid(row=1, column=2, padx=10, pady=5)
        tk.Button(controls_frame, text="Display Tree", command=self.update_tree_view, font=("Arial", 12), bg="#f0ad4e", fg="white", padx=10).grid(row=2, column=2, padx=10, pady=5)

    def update_ride_options(self, event):
        """
        Updates the Ride ID options based on the selected region.
        """
        region_rides = {
            "Kigali-Huye": ["RAD 023 H", "RAH 333 K", "RAD302 M"],
            "Kigali-Musanze": ["RAD 002 A", "RAF 212 W", "RAD322 M"],
            "Kigali-Nyagatare": ["RAC 072 V", "RAB 212 T", "RAA922 Y"],
            "Kigali-Rusizi": ["RAD 002 A", "RAF 212 W", "RAD322 M"],
            "Huye-Kigali": ["RAD 023 H", "RAH 333 K", "RAD302 M"],
            "Musanze-Kigali": ["RAD 002 A", "RAF 212 W", "RAD322 M"],
            "Rusizi-Kigali": ["RAD 002 A", "RAF 212 W", "RAD322 M"],
            "Nyagatare-Kigali": ["RAG 002 M", "RAF 212 V", "RAD322 X"]
        }
        selected_region = self.region_id_entry.get()
        self.ride_id_entry["values"] = region_rides.get(selected_region, [])

    def add_region(self):
        """
        Adds a new region node to the tree.
        """
        region_id = self.region_id_entry.get()
        if region_id:
            region_node = TreeNode(f"region_{region_id}", {"type": "region"})
            self.system.root.add_child(region_node)
            self.update_tree_view()
            CustomMessageBox(self.root, f"Region '{region_id}' added successfully!", title="Success")
        else:
            CustomMessageBox(self.root, "Please select a valid Region Name/ID.", title="Error")

    def add_ride(self):
        """
        Adds a new ride to the selected region.
        """
        region_id = self.region_id_entry.get()
        ride_id = self.ride_id_entry.get()
        ride_data = self.ride_data_entry.get()

        if not region_id or not ride_id or not ride_data:
            CustomMessageBox(self.root, "All fields (Region, Ride ID, Ride Data) must be filled.", title="Error")
            return

        self.system.add_ride(f"region_{region_id}", ride_id, ride_data)
        self.update_tree_view()
        CustomMessageBox(self.root, f"Ride '{ride_id}' added successfully under Region '{region_id}'.", title="Success")

    def update_tree_view(self):
        """
        Refreshes the Treeview to display the latest tree structure.
        """
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)
        self.system.display_tree(self.system.root, self.tree_view)

    def minimize_app(self):
        """
        Minimize the window.
        """
        self.root.iconify()

    def toggle_fullscreen(self):
        """
        Toggle fullscreen mode on and off.
        """
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

        if self.is_fullscreen:
            self.toggle_button.config(text="Exit Fullscreen")
        else:
            self.toggle_button.config(text="Maximize")

    def close_app(self):
        """
        Close the window and quit the application.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    system = TaxiBookingSystem()
    app = TaxiBookingApp(root, system)
    root.mainloop()
