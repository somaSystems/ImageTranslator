import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from converter import Converter, NoneSelected
from typing import Dict
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
    def __init__(self, root):
        self.root = root
        self.converter = Converter()
        self.root.geometry("800x700")
        self.label_ = ttk.Label(root, text="Some Image application")
        self.label_.grid(column = 2, row=0, columnspan=2, padx=5, pady=5)
        self.root.title("Image Application")
        self.radio_buttons: Dict = {}
        self.selected = []
        self._setup_cavas()
        self._images_to_radios()
        self.root.mainloop()

    def _setup_cavas(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.grid(column=0, row=4, columnspan=2, padx=5, pady=5)
        tk.Button(self.root, text="Overlay", command=self._overlay).grid(column=0, row=3, padx=5, pady=5)
        tk.Button(self.root, text="Save", command=self._save).grid(column=1, row=3, padx=5, pady=5)
    
    def _images_to_radios(self) :
        for col, key in enumerate(self.converter.all_tiffs):
            frame1 = tk.LabelFrame(self.root, text=key)
            frame1.grid(column=col, row=1, padx=5, pady=5, ipadx=5, ipady=5)
            for row, (name, image) in enumerate(self.converter.all_tiffs[key]):
                var = tk.IntVar()
                tk.Checkbutton(frame1, text=name, variable=var).grid(column=col, row=row+1)
                if key not in self.radio_buttons:
                    self.radio_buttons[key] = []
                self.radio_buttons[key].append(var)
        
    def _get_selected(self) -> Dict:
        selected = {}
        for rnds in self.radio_buttons: 
            selected[rnds] = []
            for pos, var in enumerate(self.radio_buttons[rnds]): # var = the radio button / the image
                if var.get() == 1:
                    selected[rnds].append(self.converter.all_tiffs[rnds][pos][1])
        return selected
    
    def _overlay(self):
        try:
            self.selected = self._get_selected()
            over =  self.converter.overlay(self.selected)
            self._show_image(over)
            return over
        except NoneSelected:
            messagebox.showerror("Error", "No images selected")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Something went wrong")
    
    def _show_image(self, image):
        fig = plt.figure(figsize=(5,4))
        fig = Figure(figsize = (5, 5),
                    dpi = 100)
        a = fig.add_subplot(111)
        a.imshow(image, cmap="gray")
        self.canvas = FigureCanvasTkAgg(fig,
                                master = self.root)  
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=4, columnspan=2, padx=5, pady=5)

    def _save(self):
        try:
            self.converter.save(self._overlay(), "test.png")
            messagebox.showinfo("Saved", "Image saved")
        except:
            messagebox.showerror("Error", "Image not saved, something went wrong")

    
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)