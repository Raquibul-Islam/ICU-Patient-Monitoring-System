import socket
import time
import tkinter as tk
from tkinter import messagebox
import subprocess


SERVER_IP = '127.0.0.1'
SERVER_PORT = 12004


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


root = tk.Tk()
root.title("CLIENT WINDOW")
root.geometry("700x600")


header_label = tk.Label(root, text="UDP PINGER (CLIENT SIDE)", font=("Arial", 16, "bold"), fg="blue")
header_label.pack()

def send_message():

    total_messages = 0
    successful_responses = 0

    # Clear previous results
    text_widget.delete('1.0', tk.END)

    for i in range(10):

        message = entry.get()
        start_time = time.time()
        client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

        client_socket.settimeout(2)

        try:
            response, server_address = client_socket.recvfrom(1024)
            end_time = time.time()

            rtt = end_time - start_time

            process = subprocess.Popen(["ping", "-n", "1", SERVER_IP], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate()
            ttl = "N/A"  # Default TTL value
            if "TTL=" in output:
                ttl_index = output.find("TTL=")
                ttl = output[ttl_index + 4 : ttl_index + 7]  # Extract TTL value

            # Print the received message, round-trip time, and TTL
            text_widget.insert(tk.END, f"Received response from {server_address}: {response.decode()} - RTT: {rtt:.6f}s - TTL: {ttl}\n")
            text_widget.see(tk.END)
            root.update()

            successful_responses += 1

        except socket.timeout:
            # Print timeout message
            text_widget.insert(tk.END, "Request timed out\n")
            text_widget.see(tk.END)  # Scroll to the end of the text widget
            root.update()  # Update the Tkinter window to display changes

        # Increment total_messages
        total_messages += 1

    # Calculate accuracy
    accuracy_percentage = (successful_responses / total_messages) * 100 if total_messages > 0 else 0

    # Display overall accuracy
    text_widget.insert(tk.END, f"\nOverall Accuracy: {accuracy_percentage:.2f}%\n")
    text_widget.see(tk.END)
    root.update()

label = tk.Label(root, text="Enter message to send:", font=("Arial", 12))
label.pack()
entry = tk.Entry(root, font=("Arial", 12))
entry.pack()


send_button = tk.Button(root, text="Send Message", command=send_message, bg="SKYBLUE", fg="white", font=("Arial", 12))  # Design button with color
send_button.pack()


text_widget = tk.Text(root, height=20, width=70, font=("Arial", 12))  # Increase the size of the text widget
text_widget.pack()


footer_label = tk.Label(root, text="DEVELOPED BY MD ABDUR RAKIB", font=("Arial", 12, "italic"), fg="green")
footer_label.pack()

root.mainloop()

client_socket.close()
