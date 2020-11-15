import numpy as np
import socket
from PIL import Image
import mxnet as mx


class Environment:
    def __init__(self, ip="127.0.0.1", port=13000, size=768, timescale=1):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.size = size
        self.timescale = timescale

        self.client.connect((ip, port))

    def reset(self):
        self._send(1, 0)
        return self._receive()

    def step(self, action):
        self._send(2, action)
        return self._receive()

    def state2image(self, state):
        return Image.fromarray(np.array(state, "uint8").reshape(self.size, self.size, 3))

    def _receive(self):
        # Kudos to Jan for the socket.MSG_WAITALL fix!
        data = self.client.recv(2 + 3 * self.size ** 2, socket.MSG_WAITALL)
        end = data[0]
        reward = data[1]
        state = [data[i] for i in range(2, len(data))]

        return end, reward, state

    def _send(self, action, command):
        self.client.send(bytes([action, command]))


class Episode:
    def __init__(self, environment, agent, t_threshold=100, cooldown=False):
        self.env = environment
        self.agent = agent
        self.t_threshold = t_threshold
        self.cooldown = cooldown
        self.is_win = False

    def run(self):
        end, reward, state = self.env.reset()

        # Run entire episode
        t = 0
        while not end:
            if t > self.t_threshold:
                self.env.reset()
                print("Time threshold reached. Stopping early.")
                break
            end, reward, state = self.step(reward, state)
            t += 1
        # We have won if the reward is greater than 0
        self.is_win = reward > 0

        # Additional steps if we want time for things to settle down
        if self.cooldown:
            for i in range(100):
                end, reward, state = self.step(reward, state)

    def step(self, reward, state):
        action = self.agent.step(reward, state)
        end, reward, state = self.env.step(action)
        return end, reward, state
