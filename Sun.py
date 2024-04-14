import subprocess
import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO


def upgrade_pip():
    try:
        subprocess.check_call(["python", "-m", "pip", "install", "--upgrade", "pip"])
        print("pip has been upgraded successfully!")
    except Exception as e:
        print("An error occurred while upgrading pip:", e)


def upgrade_pillow():
    try:
        subprocess.check_call(["pip", "install", "--upgrade", "pillow"])
        print("Pillow has been upgraded successfully!")
    except Exception as e:
        print("An error occurred while upgrading Pillow:", e)


def upgrade_beautifulsoup():
    try:
        subprocess.check_call(["pip", "install", "--upgrade", "beautifulsoup4"])
        print("BeautifulSoup has been upgraded successfully!")
    except Exception as e:
        print("An error occurred while upgrading BeautifulSoup:", e)


def fetch_latest_image_url(url):
    return url


class ImageViewer:
    def __init__(self, root, urls_and_names):
        self.root = root
        self.root.title("Sun Viewer")

        self.urls_and_names = urls_and_names
        self.selected_url = tk.StringVar(root, "")
        self.refresh_interval = tk.StringVar(root, "5 minutes")  # Default refresh interval is 5 minutes
        self.zoom_factor = 1.0

        self.create_widgets()

    def create_widgets(self):
        # Dropdown menu for image selection
        self.image_selection_menu = tk.OptionMenu(self.root, self.selected_url, *self.urls_and_names.keys(),
                                                  command=self.load_selected_image)
        self.image_selection_menu.pack(side="top", pady=10)

        # Display the image
        self.img_label = tk.Label(self.root)
        self.img_label.pack(expand=True, fill="both")  # Image takes all available space

        # Create a frame for the widget options
        self.widget_frame = tk.Frame(self.root)
        self.widget_frame.pack(side="top", pady=10)  # Pack the frame at the top with some padding

        # Label to display current zoom percentage
        self.zoom_label_var = tk.StringVar(self.widget_frame, "100%")
        self.zoom_label = tk.Label(self.widget_frame, textvariable=self.zoom_label_var)
        self.zoom_label.pack(side="left", padx=10)

        # Label to indicate scrolling for adjustment
        self.scroll_label = tk.Label(self.widget_frame, text="Scroll to adjust")
        self.scroll_label.pack(side="right", padx=10)

        # Dropdown menu for refresh interval
        refresh_options = ["1 minute", "2 minutes", "5 minutes", "10 minutes"]
        self.refresh_interval_menu = tk.OptionMenu(self.widget_frame, self.refresh_interval, *refresh_options)
        self.refresh_interval_menu.pack(side="left", padx=10)

        # Refresh button
        self.refresh_button = tk.Button(self.widget_frame, text="Refresh", command=self.refresh_image)
        self.refresh_button.pack(side="right", padx=10)

        # Bind mousewheel event for zooming
        self.root.bind("<MouseWheel>", self.zoom_image)

        # Load the first image by default
        self.load_selected_image()

    def load_selected_image(self, *args):
        selected_name = self.selected_url.get()
        selected_url = self.urls_and_names.get(selected_name, "")
        if selected_url:
            image_data = requests.get(selected_url).content
            image = Image.open(BytesIO(image_data))
            self.rendered_image = image
            photo = ImageTk.PhotoImage(image)
            self.img_label.configure(image=photo)
            self.img_label.image = photo
            self.zoom_factor = 1.0
            self.update_zoom_label()

    def zoom_image(self, event):
        # Zoom in or out based on mouse wheel movement
        if event.delta > 0:
            self.zoom_factor *= 1.1  # Zoom in
        else:
            self.zoom_factor /= 1.1  # Zoom out

        # Apply zoom to the image
        width = int(self.rendered_image.width * self.zoom_factor)
        height = int(self.rendered_image.height * self.zoom_factor)
        resized_image = self.rendered_image.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        self.img_label.configure(image=photo)
        self.img_label.image = photo
        self.update_zoom_label()

    def update_zoom_label(self):
        # Update the zoom label with the current zoom percentage
        zoom_percentage = int(self.zoom_factor * 100)
        self.zoom_label_var.set(f"{zoom_percentage}%")

    def refresh_image(self):
        new_interval = self.refresh_interval.get().split()[0]  # Extract the interval value (e.g., "5")
        interval_seconds = int(new_interval) * 60 * 1000  # Convert to milliseconds
        self.root.after(interval_seconds, self.refresh_image)  # Schedule the next refresh
        self.load_selected_image()


if __name__ == "__main__":
    root = tk.Tk()

    urls_and_names = {
        "1024 PFSS - AIA 193 Å": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0193pfss.jpg",
        "1024 PFSS - AIA 211 Å": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0211pfss.jpg",
        "1024 PFSS - AIA 171 Å": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171pfss.jpg",
        "1024 PFSS - AIA 211 Å, 193 Å, 171 Å": "https://sdo.gsfc.nasa.gov/assets/img/latest/f_211_193_171pfss_1024.jpg"
    }

    image_viewer = ImageViewer(root, urls_and_names)
    root.mainloop()
