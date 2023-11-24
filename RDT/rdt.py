import random
import time

class RDTSender:
    def __init__(self, channel):
        self.channel = channel
        self.seq_num = 0

    def rdt_send(self, data, receiver):
        packet = self.make_packet(data)
        self.send_packet(packet)
        while True:
            ack_received = receiver.rdt_receive(packet)
            if ack_received:
                break
            else:
                print(f"Timeout: Resending packet with sequence number {packet['sequence_number']}")
                self.send_packet(packet)

    def send_packet(self, packet):
        self.channel.send(packet)

    def make_packet(self, data):
        packet = {'sequence_number': self.seq_num, 'data': data}
        self.seq_num = 1 - self.seq_num  # Toggle sequence number (0 or 1)
        return packet


class RDTReceiver:
    def __init__(self, channel):
        self.channel = channel

    def rdt_receive(self, sender_packet):
        received_packet = self.receive_packet()
        if received_packet and received_packet['sequence_number'] == sender_packet['sequence_number']:
            print(f"Received {received_packet['data']} with sequence number {received_packet['sequence_number']}")
            self.send_acknowledgement(received_packet['sequence_number'])
            return True  # Acknowledgment received successfully
        else:
            return False  # Acknowledgment not received

    def receive_packet(self):
        return self.channel.receive()

    def send_acknowledgement(self, seq_num):
        ack = {'acknowledgement': seq_num}
        print(f"Sending ACK{seq_num}")
        self.channel.send(ack)


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

# Example usage:
if __name__ == "__main__":
    channel = SimulatedChannel()
    sender = RDTSender(channel)
    receiver = RDTReceiver(channel)

    with open("test_rdt.txt", "r") as file:
        for line in file:
            data, content = line.strip().split(' ', 1)
            sender.rdt_send((data, content), receiver)
