import socket
import random
import time
import tkinter as tk

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12004

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

root = tk.Tk()
root.title("Server Window")
root.geometry("700x600")

header_label = tk.Label(root, text="UDP PINGER (SERVER SIDE)", font=("Arial", 16, "bold"), fg="blue")
header_label.pack()

text_widget = tk.Text(root, height=30, width=70, font=("Arial", 12))  # Increased height to accommodate more text
text_widget.pack()

footer_label = tk.Label(root, text="DEVELOPED BY MD ABDUR RAKIB", font=("Arial", 12, "italic"), fg="green")
footer_label.pack(side=tk.BOTTOM)


def update_interface():

    message, client_address = server_socket.recvfrom(1024)
    start_time = time.time()


    if random.randint(1, 10) <= 2:
        lost_packet_message = "Packet loss simulated.\n"
        text_widget.insert(tk.END, f"{lost_packet_message}\n")
        text_widget.see(tk.END)  # Scroll to the end of the text widget
        root.after(1000, update_interface)  # Continue updating interface
        return

    random_delay = random.uniform(0, 2)
    time.sleep(random_delay)


    server_socket.sendto(message, client_address)

    # Calculate RTT
    end_time = time.time()
    rtt = end_time - start_time

    received_message = f"Received message from {client_address}: {message.decode()} - RTT: {rtt:.6f}s"
    response_info = f"Response from {SERVER_IP}:{SERVER_PORT} - Message: {message.decode()}"
    text_widget.insert(tk.END, f"{received_message}\n{response_info}\n")
    text_widget.see(tk.END)
    root.after(1000, update_interface)


update_interface()

root.mainloop()
