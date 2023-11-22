import random

class AIMDCongestionControl:
    def __init__(self, initial_window_size, max_window_size, min_window_size, increase_factor, decrease_factor, loss_probability):
        self.window_size = initial_window_size
        self.max_window_size = max_window_size
        self.min_window_size = min_window_size
        self.increase_factor = increase_factor
        self.decrease_factor = decrease_factor
        self.loss_probability = loss_probability

    def simulate_network(self):
        # Simulate a network with packet loss
        return random.random() > self.loss_probability

    def send_packet(self):
        if self.window_size < self.max_window_size:
            self.window_size += self.increase_factor

    def receive_ack(self, successful_transmission):
        if successful_transmission:
            if self.window_size > self.min_window_size:
                self.window_size *= self.increase_factor
        else:
            self.window_size *= self.decrease_factor
            if self.window_size < self.min_window_size:
                self.window_size = self.min_window_size

    def run_simulation(self, num_iterations):
        for _ in range(num_iterations):
            if self.simulate_network():
                # Packet successfully transmitted
                self.send_packet()
                self.receive_ack(True)
                print(f"Window size: {self.window_size} (Successful transmission)")
            else:
                # Packet lost
                self.receive_ack(False)
                print(f"Window size: {self.window_size} (Packet loss)")

# Example usage:
initial_window_size = 10
max_window_size = 100
min_window_size = 1
increase_factor = 2
decrease_factor = 0.5
loss_probability = 0.3

aimd = AIMDCongestionControl(initial_window_size, max_window_size, min_window_size, increase_factor, decrease_factor, loss_probability)
aimd.run_simulation(100)
