import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import pytesseract

# Path to Tesseract executable (Update this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define the decoding and encoding dictionary
decode_map = {
    "01": "a", "10": "b", "001": "c", "100": "d", "02": "e", "20": "f",
    "002": "g", "200": "h", "03": "i", "30": "j", "003": "k", "300": "l",
    "04": "m", "40": "n", "004": "o", "400": "p", "05": "q", "50": "r",
    "005": "s", "500": "t", "06": "u", "60": "v", "006": "w", "600": "x",
    "07": "y", "70": "z"
}

# Reverse the dictionary for encoding
encode_map = {v: k for k, v in decode_map.items()}

# Function to decode the input code
def decode_code_language(input_code):
    words = input_code.split()  # Split input into words
    decoded_message = []
    for word in words:
        letters = word.split(",")  # Split word into letters
        decoded_word = "".join(decode_map.get(letter, "?") for letter in letters)
        decoded_message.append(decoded_word)  # Append decoded word to the message
    return " ".join(decoded_message)

# Function to encode text back to code
def encode_code_language(input_text):
    encoded_message = []
    for word in input_text.split():
        encoded_word = ",".join(encode_map.get(char, "?") for char in word.lower())
        encoded_message.append(encoded_word)
    return " ".join(encoded_message)

# Function to handle image upload and text extraction
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        try:
            # Load the image
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, text.strip())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")

# Function to decode the text
def decode():
    input_code = input_text.get("1.0", tk.END).strip()
    if not input_code:
        messagebox.showwarning("Warning", "Please enter a code or upload an image!")
        return
    try:
        decoded_message = decode_code_language(input_code)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decoded_message)
        output_text.config(state=tk.NORMAL)  # Allow user to edit the decoded text
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to encode the text
def encode():
    input_message = output_text.get("1.0", tk.END).strip()
    if not input_message:
        messagebox.showwarning("Warning", "Please enter text to encode in the decoded section!")
        return
    try:
        encoded_message = encode_code_language(input_message)
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, encoded_message)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to save the decoded text to a file
def save_decoded_text():
    decoded_content = output_text.get("1.0", tk.END).strip()
    if not decoded_content:
        messagebox.showwarning("Warning", "Nothing to save. Please decode text first!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(decoded_content)
            messagebox.showinfo("Success", "Decoded text saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

# Function to clear the decoded text area
def clear_decoded_text():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)

# Create the main application window
root = tk.Tk()
root.title("Mysterious Decoder with OCR")
root.geometry("800x600")
root.configure(bg="#121212")
root.minsize(800, 600)

# Modern fonts and styling
HEADER_FONT = ("Segoe UI", 18, "bold")
BUTTON_FONT = ("Segoe UI", 12, "bold")
TEXT_FONT = ("Consolas", 12)

# Title Header
header_label = tk.Label(root, text="Enter the code to decode or upload an image:", font=HEADER_FONT, fg="white", bg="#121212")
header_label.pack(pady=10)

# Input Text Box
input_frame = tk.Frame(root, bg="#121212")
input_frame.pack(fill=tk.BOTH, padx=20, pady=5)
input_text = tk.Text(input_frame, font=TEXT_FONT, wrap=tk.WORD, bg="#1e1e1e", fg="white", insertbackground="white", relief=tk.FLAT, height=10)
input_text.pack(fill=tk.BOTH, expand=True)

# Buttons Frame
buttons_frame = tk.Frame(root, bg="#121212")
buttons_frame.pack(pady=10)

upload_button = tk.Button(buttons_frame, text="Upload Image", font=BUTTON_FONT, fg="white", bg="#8a2be2", activebackground="#7a1ccf", command=upload_image)
upload_button.grid(row=0, column=0, padx=10)

decode_button = tk.Button(buttons_frame, text="Decode", font=BUTTON_FONT, fg="white", bg="#32cd32", activebackground="#2dbb2d", command=decode)
decode_button.grid(row=0, column=1, padx=10)

save_button = tk.Button(buttons_frame, text="Save Decoded Text", font=BUTTON_FONT, fg="white", bg="#1e90ff", activebackground="#187bcd", command=save_decoded_text)
save_button.grid(row=0, column=2, padx=10)

clear_button = tk.Button(buttons_frame, text="Clear Decoded Text", font=BUTTON_FONT, fg="white", bg="#ff4500", activebackground="#e03c00", command=clear_decoded_text)
clear_button.grid(row=0, column=3, padx=10)

encode_button = tk.Button(buttons_frame, text="Encode", font=BUTTON_FONT, fg="white", bg="#ffa500", activebackground="#e69500", command=encode)
encode_button.grid(row=0, column=4, padx=10)

# Decoded Message Header
output_header = tk.Label(root, text="Decoded Message:", font=HEADER_FONT, fg="white", bg="#121212")
output_header.pack(pady=(20, 5))

# Output Text Box
output_frame = tk.Frame(root, bg="#121212")
output_frame.pack(fill=tk.BOTH, padx=20, pady=5, expand=True)
output_text = tk.Text(output_frame, font=TEXT_FONT, wrap=tk.WORD, bg="#1e1e1e", fg="white", insertbackground="white", relief=tk.FLAT)
output_text.pack(fill=tk.BOTH, expand=True)

# Start the main loop
root.mainloop()
