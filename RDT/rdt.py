import socket
import random
from multiprocessing import Process

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def sender(message, loss_probability):
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender_socket.bind(('127.0.0.1', 12345))

    for i in range(len(message)):
        packet = message[i]
        sender_socket.sendto(packet.encode(), ('127.0.0.1', 54321))
        print(f"Sender---Sent: {packet}")

        if random.random() > loss_probability:
            try:
                sender_socket.settimeout(2)
                ack, _ = sender_socket.recvfrom(1024)
                if ack.decode() == "ACK":
                    print("Sender----Received ACK\n")
                else:
                    print("Sender----Received NAK, Resending\n")
                    i -= 1  # Retransmit the current packet
            except socket.timeout:
                print("Sender----Timeout, Resending\n")
                i -= 1  # Retransmit the current packet

    sender_socket.close()

def receiver():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(('127.0.0.1', 54321))

    while True:
        data, addr = receiver_socket.recvfrom(1024)
        if random.random() > 0.2:  # Simulate 20% packet loss
            receiver_socket.sendto("ACK".encode(), addr)
            print(f"Reciever----Received: {data.decode()}, Sent ACK\n")
        else:
            print("Packet lost, Sending NAK\n")

if __name__ == "__main__":
    file_path = "test_rdt.txt"  # Replace with your file path
    message = read_file(file_path)
    loss_probability = 0.3  # Simulate 20% packet loss

    receiver_process = Process(target=receiver)
    sender_process = Process(target=sender, args=(message, loss_probability))

    receiver_process.start()
    sender_process.start()

    receiver_process.join()
    sender_process.join()
