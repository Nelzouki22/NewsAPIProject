import tkinter as tk
from tkinter import messagebox, Scrollbar, RIGHT, Y
import requests
import csv
import webbrowser

# Function to fetch news using News API
def get_news(api_key, category, country):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country={country}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "ok":
        news_list.delete(0, tk.END)  # Clear previous news
        news_data.clear()  # Clear previous news data
        for i, article in enumerate(data["articles"][:10], 1):
            news_list.insert(tk.END, f"{i}. {article['title']}")
            news_list.insert(tk.END, article['url'])
            news_data.append(article)  # Save the news data for the save function
    else:
        messagebox.showerror("Error", "Error fetching news!")

# Function to handle fetch button click
def fetch_news():
    category = category_entry.get()
    country = country_entry.get()
    if category and country:
        get_news(api_key, category, country)
    else:
        messagebox.showerror("Input Error", "Please enter both category and country.")

# Function to open news link in browser
def open_link(event):
    selected = news_list.get(news_list.curselection())
    if selected.startswith("http"):
        webbrowser.open(selected)

# Function to save news to CSV
def save_news_to_csv():
    if news_data:
        with open('news.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "URL"])
            for article in news_data:
                writer.writerow([article['title'], article['url']])
        messagebox.showinfo("Saved", "News saved to news.csv")
    else:
        messagebox.showerror("No Data", "No news data to save! Please fetch news first.")

# Set your API key
api_key = "4be6856d37b7495cb0e5800a8f92a74b"
news_data = []

# Set up the GUI with better layout
root = tk.Tk()
root.title("News API")
root.geometry("800x600")  # Set a larger window size
root.resizable(True, True)  # Allow resizing

# Input fields with labels
tk.Label(root, text="Category:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
category_entry = tk.Entry(root, font=("Arial", 14))  # Increase font size
category_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

tk.Label(root, text="Country:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
country_entry = tk.Entry(root, font=("Arial", 14))  # Increase font size
country_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

# Fetch button
fetch_button = tk.Button(root, text="Fetch News", command=fetch_news, bg="#4CAF50", fg="white", font=("Arial", 14))
fetch_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='we')

# News listbox with scrollbar
frame = tk.Frame(root)
frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='we')
scrollbar = Scrollbar(frame, orient="vertical")
news_list = tk.Listbox(frame, width=100, height=20, font=("Arial", 12), yscrollcommand=scrollbar.set)  # Increased width and height
scrollbar.config(command=news_list.yview)
scrollbar.pack(side=RIGHT, fill=Y)
news_list.pack(side="left", fill="both", expand=True)

# Save button
save_button = tk.Button(root, text="Save News to CSV", command=save_news_to_csv, bg="#008CBA", fg="white", font=("Arial", 14))
save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='we')

# Double-click to open news link
news_list.bind('<Double-1>', open_link)

# Run the GUI main loop
root.mainloop()
