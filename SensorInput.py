import pyautogui

class SensorInput:
  
  def __init__(self, input):
    self.input = input
  
  def get_sensor_value(self):
    return self.input()
  
