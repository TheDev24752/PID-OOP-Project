import pyautogui

class SensorInput:
  
  def __init__(self, input):
    self.input = input
  
  def get_sensor_value(self):
    return self.input()

    # return 1

  # obselete
  def get_funct_value(PIDoutput):
    return (PIDoutput * 100 ** 0.5) - 2 #just a random function
