# Description: This file contains the class that will handle the client's connection to the server and the robot.
class Client:
    def __init__(self, name):
        self.name = name
        self.connection_state = 0
        
    def get_name(self):
        return self.name
    
    def get_connection_state(self):
        return self.connection_state
    
    def set_connection_state(self, state):
        self.connection_state = state
        pass