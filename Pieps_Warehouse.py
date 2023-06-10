import ttkbootstrap as ttk
import tkinter.filedialog as filedialog
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import *
from PIL import Image, ImageTk
import csv
import webbrowser

class IMS:
    def __init__(self, root):
        # Init IMS Main Class
        self.root = root
        self.root.title("Pieps Warehouse v1.0")
        self.root.maxsize(1400, 800)
        self.root.minsize(1400, 800)

        #Image
        self.image = Image.open("Logo.png").resize((250, 200))
        self.photo = ImageTk.PhotoImage(self.image)

        
        # Calculate Window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1400
        window_height = 800
        
        # Calculate window position
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        
        # Set Window posistion
        self.root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
        
        # Set Variable for Class 
        self.window_width = window_width
        self.window_height = window_height
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Data Store Vari
        self.data = []
        

        # Set Mainbar
        self.navbar = ttk.Frame(root, padding="5 10", style="TButton", height=10)
        self.navbar.pack(side="top", fill="x")

        #info Label
        my_font = ttk.font.Font(size=15)
        self.info_label = ttk.Label(root, text="Artikel", font=my_font)
        self.info_label.pack(side="top")

        # Navbar Buttons
        self.navbar_button1 = ttk.Menubutton(self.navbar, text="Datei")
        self.navbar_button1.pack(side="left", padx=10)
        self.create_dropdown(self.navbar_button1)
        self.navbar_button2 = ttk.Menubutton(self.navbar, text="Über Uns")
        self.navbar_button2.pack(side="left", padx=10)
        self.create_dropdown2(self.navbar_button2)

         # Add new item Frame
        self.add_item_frame = ttk.Frame(root, padding="10")
        self.add_item_frame.pack(side="left", fill="y")

        # Add new item Labels and Entry widgets
        ttk.Label(self.add_item_frame, text="Artikel:").grid(row=0, column=0, sticky="w")
        self.artikel_entry = ttk.Entry(self.add_item_frame)
        self.artikel_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_item_frame, text="Bezeichnung:").grid(row=1, column=0, sticky="w")
        self.bezeichnung_entry = ttk.Entry(self.add_item_frame)
        self.bezeichnung_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_item_frame, text="Menge:").grid(row=2, column=0, sticky="w")
        self.menge_entry = ttk.Entry(self.add_item_frame)
        self.menge_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_item_frame, text="Artikelnummer:").grid(row=3, column=0, sticky="w")
        self.artikelnummer_entry = ttk.Entry(self.add_item_frame)
        self.artikelnummer_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.add_item_frame, text="Hinzufügen", command=self.add_new_item).grid(row=4, column=0, padx=5, pady=10)
        ttk.Button(self.add_item_frame, text="Speichern", command=self.quick_save).grid(row=4, column=1, padx=5, pady=10)


        # Add Table Frame
        self.table_frame = ttk.Frame(root, padding="10")
        self.table_frame.pack(side="right", fill="both", expand=True)

        # Create Table
        self.table = self.create_table()

    
        #photo placement
        photo_label = ttk.Label(root, image=self.photo, text="by Freelance Archery", compound="top")
        photo_label.config()
        photo_label.place(x=0, y=550)

        self.file_path = "tabledata.csv"  # Pfad zur CSV-Datei
        if self.check_file_exists(self.file_path):
            self.load_data_from_file(self.file_path)
        else:
            # Create empty file
            self.save_data_to_file(self.file_path)

    def openbrowser(self):
        webbrowser.open_new_tab("www.freelance-archery.de")


        # Create and set function in Dropdown
    def create_dropdown(self, button):
        dropdown = ttk.Menu(button, tearoff=False)
        dropdown.add_command(label="Öffnen", command=self.open_file)
        dropdown.add_command(label="Speichern unter", command=self.save_table)
        dropdown.add_command(label="Beenden", command=self.exit_programm)

        button["menu"] = dropdown

        # Create Second dropdownset
    def create_dropdown2(self, button):
        dropdown = ttk.Menu(button, tearoff=False)
        dropdown.add_command(label="www.freelance-archery.de", command=self.openbrowser)

        button["menu"] = dropdown

        # Create Tabel
    def create_table(self):
        coldata = [
            {"text": "Artikel/Material", "width": 300},
            {"text": "Beschreibung", "width": 350},
            {"text": "Menge"},
            {"text": "Artikelnummer", "width": 276},
            ]
        self.table = Tableview(
            master=self.root,
            rowdata=self.data,
            coldata=coldata,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            height=25,
            pagesize=25
            )
        self.table.pack(fill="both", expand=True)
        

        # Add Data to Table
        for data_item in self.data:
            self.table.insert_row(data_item)

        return self.table
    
    

        # Get Input to add Item(Row)
    def add_new_item(self):
        artikel = self.artikel_entry.get()
        bezeichnung = self.bezeichnung_entry.get()
        menge = self.menge_entry.get()
        artikelnummer = self.artikelnummer_entry.get()

        # Add new item to data list
        self.data = [row.values for row in self.table.tablerows]
        new_item = (artikel, bezeichnung, menge, artikelnummer)
        self.data.append(new_item)

        # Clear Entry Fields
        self.artikel_entry.delete(0, 'end')
        self.bezeichnung_entry.delete(0, 'end')
        self.menge_entry.delete(0, 'end')
        self.artikelnummer_entry.delete(0, 'end')

        #Toast Popup Notification
        toast = ToastNotification(
            title="Übermittlung erfolgreich",
            message="Daten erfolgreich eingegeben",
            duration=3000
        )
        toast.show_toast()


        # Update Table
        self.table.destroy()
        self.table = self.create_table()


    #save table to csv
    def save_table(self):
            records = [row.values for row in self.table.tablerows]
            self.table.save_data_to_csv(records=records)


    def check_file_exists(self, file_path):
        try:
            with open(file_path, 'r'):
                return True
        except FileNotFoundError:
            return False

    #Save Data to file
    def save_data_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for data_item in self.data:
                file.write(','.join(map(str, data_item)) + '\n')

    #read data from file
    def load_data_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.data = [tuple(line.strip().split(',')) for line in file.readlines()]
                self.table.destroy()
                self.table = self.create_table()

        except FileNotFoundError:
            #Toast Popup Notification
            toast = ToastNotification(
            title="Warnung",
            message="Keine Datei gefunden",
            duration=3000
            )
            toast.show_toast()


     # Open File
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV File", "*.CSV"), ("Text File", "*.txt"), ("All Files", "*.*")])
        if file_path:
            print("Datei ausgewählt: " + file_path)
            self.load_data_from_file(file_path)

    # Save File
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.CSV"), ("All Files", "*.*")])
        if file_path:
            print("Datei gespeichert unter: " + file_path)
            self.save_data_to_file(file_path)

    def quick_save(self):
        records = [row.values for row in self.table.tablerows]
        self.save_to_csv(records=records)

    def save_to_csv(self, records, delimiter=','):
        filename = "tabledata.csv"  # Statischer Dateiname und Pfad
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerows(records)

        #Toast Popup Notification
        toast = ToastNotification(
            title="Daten gespeichert",
            message="Daten erfolgreich gespeichert",
            duration=3000
        )
        toast.show_toast()

        # Exit App
    def exit_programm(self):
        self.root.destroy()



# Main Root Function
root = ttk.Window(themename="solar")
main = IMS(root)

root.mainloop()