import pyautogui

class SensorInput:
  
  def __init__():
    self.pin_location
  
  def get_sensor_value():
    return pyautogui.position()[1]  #gets the mouse's y-position

    # return 1
  
  def get_funct_value(PIDoutput):
    return (PIDoutput * 100 ** 0.5) - 2 #just a random function
