import PID_Auto_Tuning
import SensorInput
import pyautogui
import time

def changeY(change):
  pyautogui.moveTo(pyautogui.position()[0], pyautogui.position()[1] + change)

setpoint = 100

sensor = SensorInput()
controller = PID_Auto_Tuning(setpoint)

controller.ziegler_nicholas_PID(sensor, changeY)

inputs = []
times = []

inputs.append(sensor.get_sensor_value())
times.append(time.process_time_ns())

while True:
  inputs.append(sensor.get_sensor_value())
  times.append(time.process_time_ns())
  changeY(controller.PID(inputs, times))
