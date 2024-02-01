import tkinter as tk
from tkinter import messagebox
import requests

API_ADD_ENDPOINT = "http://127.0.0.1:5000/cars"

class AddCarPopup(tk.Frame):
    """ Popup Frame to Add a Book """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        # The Add Point Form Widgets
        tk.Label(self, text="Make:").grid(row=2, column=1)
        self._make = tk.Entry(self)
        self._make.grid(row=2, column=2)
        tk.Label(self, text="Model:").grid(row=3, column=1)
        self._model = tk.Entry(self)
        self._model.grid(row=3, column=2)
        tk.Label(self, text="Year:").grid(row=4, column=1)
        self._year = tk.Entry(self)
        self._year.grid(row=4, column=2)
        tk.Label(self, text="Price:").grid(row=5, column=1)
        self._price = tk.Entry(self)
        self._price.grid(row=5, column=2)
        tk.Button(self, text="Submit", command=self._submit_cb).grid(row=6, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(row=6, column=2)

    def _submit_cb(self):
        """ Submit the Add Book """

        data = {}
        data['make'] = self._make.get()
        data['model'] = self._model.get()
        data['year'] = int(self._year.get())
        data['price'] = float(self._price.get())

        headers = {"content-type": "application/json"}
        response = requests.post(API_ADD_ENDPOINT, json=data, headers=headers)

        if response.status_code == 200:
            self._close_cb()
        else:
            messagebox.showerror("Error", "Cannot add car because: " + response.text)


