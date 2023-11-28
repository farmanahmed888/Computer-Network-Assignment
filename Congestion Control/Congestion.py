import random

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

class CongestionControl:
    def __init__(self, channel, slow_start_threshold=10, congestion_window=1):
        self.channel = channel
        self.slow_start_threshold = slow_start_threshold
        self.congestion_window = congestion_window

    def send_data(self, data):
        print(f"Initial Congestion Window Size: {self.congestion_window}")

        for step in range(100):  # Sending 100 data packets
            window_data = data[:self.congestion_window]
            packet = self.make_packet(window_data)
            self.send_packet(packet)
            ack_received = self.receive_ack()

            if ack_received:
                # Slow-start phase: Exponentially increase the congestion window size
                if self.congestion_window < self.slow_start_threshold:
                    self.congestion_window = min(self.congestion_window * 2, self.slow_start_threshold)
                else:
                    # AIMD phase: Increase congestion window additively
                    self.congestion_window += 1
                
            else:
                # Timeout or loss, reduce congestion window multiplicatively (MD)
                print("Loss happened due to timeout...")
                self.slow_start_threshold = max(self.congestion_window // 2, 1)
                self.congestion_window = 1

            data = data[min(self.congestion_window, len(data)):]

            print(f"Step {step + 1}: Congestion Window Size: {self.congestion_window}")

    def send_packet(self, packet):
        # Send packet over the network (simulated by the SimulatedChannel)
        self.channel.send(packet)

    def make_packet(self, data):
        # Construct packet with data and size
        return {"data": data, "size": len(data)}

    def receive_ack(self):
        # Receive acknowledgement from the receiver (simulated by the SimulatedChannel)
        return self.channel.receive()


channel = SimulatedChannel(loss_rate=0.3)  # Adjust loss rate as needed
congestion_control = CongestionControl(channel)

# Test with a data stream
data_stream = "Pkt" * 100  # 100 packets of the same data for simplicity
congestion_control.send_data(data_stream)

