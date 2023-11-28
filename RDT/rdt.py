import random
import time

class SimulatedChannel:
    def __init__(self, loss_rate=0.3):
        self.loss_rate = loss_rate
        self.packet = None
    
    def send(self, packet):
        if random.random() >= self.loss_rate:
            self.packet = packet
        else:
            self.packet = None
    
    def receive(self):
        if random.random() >= self.loss_rate:
            return self.packet
        return None

class StopAndWaitRDT:
    def __init__(self, channel):
        self.channel = channel
        self.sequence_number = 0

    def send_data(self, data, content):
        packet = {"data": data, "content": content, "seq_num": self.sequence_number}
        print(f"Sending {data} - {content} with sequence number {self.sequence_number}")
        self.send_packet(packet)

        # Wait for ACK
        ack_received = self.receive_ack()
        if ack_received == self.sequence_number:
            print(f"Received ACK {ack_received}. Transmission successful")
            self.sequence_number = 1 - self.sequence_number  # Toggle sequence number (0 or 1)
        else:
            print(f"Timeout Occurred. Retransmitting data")
            self.send_data(data, content)  # Retransmit if ACK not received

    def send_packet(self, packet):
        # Send packet over the network
        self.channel.send(packet)

    def receive_ack(self):
        # Receive ACK from the receiver
        ack_packet = self.channel.receive()
        if ack_packet is not None:
            return ack_packet["seq_num"]
        return None

class StopAndWaitReceiver:
    def __init__(self, channel):
        self.channel = channel

    def receive_data(self):
        packet = self.channel.receive()
        if packet is not None:
            print(f"Received {packet['data']} - {packet['content']} with sequence number {packet['seq_num']}")
            self.send_ack(packet)

    def send_ack(self, packet):
        # Send ACK to the sender
        ack_packet = {"seq_num": packet["seq_num"]}
        self.channel.send(ack_packet)

# Example usage:
channel = SimulatedChannel()
sender = StopAndWaitRDT(channel)
receiver = StopAndWaitReceiver(channel)

# Read data from file
with open("test_rdt.txt", "r") as file:
    data_list = [line.strip().split(" ", 1) for line in file]

for data, content in data_list:
    sender.send_data(data, content)
    receiver.receive_data()
    time.sleep(1)
