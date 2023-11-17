import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import psycopg2
import tkinter as tk
from tkinter import simpledialog, messagebox

# Define the PostgreSQL database connection parameters
db_params = {
    'host': 'localhost',
    'dbname': 'inventory',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432',
}

# File to store trolley IDs
trolley_file_path = 'trolley_ids.txt'

# File to store scanned items details
scanned_items_file_path = 'scanned_items.txt'

# Initialize the RFID reader
reader = SimpleMFRC522()

# Create a set to store scanned RFID UIDs
scanned_uids = set()

# Initialize tkinter
root = tk.Tk()
root.title("RFID Scanning and Payment Display")
root.geometry("1920x1080")  # Set screen size

# Create tkinter labels for displaying information
total_price_label = tk.Label(root, text="Total Price: $0.00", font=("Times New Roman", 30, "bold"))
item_info_label = tk.Label(root, text="Items in Trolley:", font=("Times New Roman", 30, "bold"))
item_listbox = tk.Listbox(root, width=50, height=10, font=("Times New Roman", 30))

# Pack labels to display
total_price_label.pack()
item_info_label.pack()
item_listbox.pack()

# Variables to store data
total_price = 0.0

# Function to retrieve and display the combined table
def display_combined_table(cursor, trolley_id):
    cursor.execute("SELECT item_price.item_uid, item_price.price, table_trolley.item FROM item_price JOIN table_trolley ON item_price.item_uid = table_trolley.item_uid WHERE table_trolley.trolley_id = %s", (trolley_id,))
    combined_table = cursor.fetchall()
    return combined_table

# Function to handle payment
import math

# Function to check if trolley ID is in the file
def check_trolley_id(trolley_id):
    with open(trolley_file_path, 'r') as file:
        trolley_ids = file.read().splitlines()
    return str(trolley_id) in trolley_ids

# Function to write trolley ID to the file
def write_trolley_id(trolley_id):
    with open(trolley_file_path, 'a') as file:
        file.write(str(trolley_id) + '\n')

# Function to write scanned items to the file
def write_scanned_items_to_file(trolley_id, scanned_items):
    with open(scanned_items_file_path, 'a') as file:
        file.write(f"Trolley ID: {trolley_id}\n")
        for item_uid, item_price, item_name in scanned_items:
            file.write(f"Item UID: {item_uid}, Item Name: {item_name}, Item Price: ${item_price:.2f}\n")
        file.write("\n")

def display_items_in_listbox():
    # Clear the listbox
    item_listbox.delete(0, tk.END)

    # Display item details at the top
    item_listbox.insert(tk.END, "Item UID\tItem Name\tItem Price")
    item_listbox.insert(tk.END, "="*50)

    # Display each item in the listbox
    total_price = 0.0  # Initialize total price

    for item_uid, item_price, item_name in combined_table:
        uid_str = f"{item_uid}"
        name_str = f"{item_name}"
        price_str = f"${item_price:.2f}"

        # Concatenate strings for UID, name, and price
        info = f"{uid_str}\t{name_str}\t{price_str}"

        # Insert concatenated string into the listbox
        item_listbox.insert(tk.END, info)

        # Update total price
        total_price += item_price

    # Update the total price label
    total_price_label.config(text=f"Total Price: ${total_price:.2f}")


def make_payment():
    # Prompt for account number (trolley ID)
    trolley_id = simpledialog.askinteger("Payment", "Enter Account Number (Trolley ID):", parent=root)

    # Calculate the total price
    total_price = sum(item_price for _, item_price, _ in combined_table)

    # Check if the entered trolley ID is in the file
    if not check_trolley_id(trolley_id):
        messagebox.showerror("Error", "Wrong Account Number. Account number should match the trolley ID.")
        return

    # Display prompt for the amount payable
    amount_payable = simpledialog.askfloat("Payment", f"Amount Payable: ${total_price:.2f}\nEnter Amount Paid:", parent=root)
    if amount_payable is None:
        return  # User canceled the prompt

    # Check if the payment is close enough to the total price
    if not math.isclose(amount_payable, total_price, rel_tol=1e-9):
        messagebox.showerror("Payment Error", "Incorrect amount paid.")
        return

    # Process payment (you can customize this part based on your payment system)
    # For now, just display a success message
    messagebox.showinfo("Payment Success", "Payment successful! Thank you for shopping with us!")

    # Update the database and remove items from the trolley
    for item_uid, _, _ in combined_table:
        cursor.execute("DELETE FROM table_trolley WHERE item_uid = %s", (item_uid,))
        conn.commit()

    # Clear the listbox and update the tkinter labels
    item_listbox.delete(0, tk.END)

    # Disable the payment button
    pay_button.config(state=tk.DISABLED)

    # Write the scanned items details to the file
    write_scanned_items_to_file(trolley_id, combined_table)

    # Display items in the listbox
    display_items_in_listbox()



    # Disable the payment button
    pay_button.config(state=tk.DISABLED)

# Button to trigger payment
pay_button = tk.Button(root, text="Make Payment", command=make_payment, state=tk.DISABLED, font=("Times New Roman", 30))
pay_button.pack()

try:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    while True:
        try:
            # Read the RFID tag
            print('Please place your RFID Tag: ')
            id, _ = reader.read()
            print(id)

            # Check if this UID has already been scanned
            if id not in scanned_uids:
                # Check if it's a trolley UID
                cursor.execute("SELECT trolley_id FROM table_trolley WHERE trolley_id = %s", (str(id),))
                trolley_result = cursor.fetchone()

                if trolley_result:
                    # If it's a trolley UID, join the tables and display the items in the trolley
                    trolley_id = trolley_result[0]

                    combined_table = display_combined_table(cursor, trolley_id)
                    display_items_in_listbox()
                    

                    # Enable the payment button
                    pay_button.config(state=tk.NORMAL)

                    # Write the trolley ID to the file
                    write_trolley_id(trolley_id)

                else:
                    # Display a notification if it's not a trolley UID
                    print("Scanned item is not in the database")
                    break

                scanned_uids.add(id)
                root.update()

        except KeyboardInterrupt:
            break

finally:
    # Clean up and close the database connection
    cursor.close()
    conn.close()
    GPIO.cleanup()

root.mainloop()
