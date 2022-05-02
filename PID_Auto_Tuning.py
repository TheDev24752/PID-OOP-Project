from datetime import datetime
from PIDController import PIDController


class PIDAutoTuning(PIDController):

  def __init__(self, setpoint):
    super().__init__(setpoint)
  
  def ziegler_nichols_PID(self, sensor, output, step_size = 0.1, error_range = 0.1): # pass through sensor object, output method, optionally step size and error
    self.kp = 1
    self.ki = 0
    self.kd = 0
    max1 = 0
    min = sensor.get_sensor_value()
    max2 = 0
    t1 = 0
    t2 = 0
    while True:
      for i in range(2): # run system for 3 periods, so that it can settle into oscillation
        m = sensor.get_sensor_value()
        output(self.P([m], []))
        while min >= m: # make sure the graph is going up before we find the maximum
          min = m
          m = sensor.get_sensor_value()
          output(self.P([m], []))
        max1 = m
        m = sensor.get_sensor_value()
        output(self.P([m], []))
        while max1 <= m:
          max1 = m
          m = sensor.get_sensor_value()
          output(self.P([m], []))
        min = m
        t1 = datetime.now().time().hour * 24 * 60 * 60 + datetime.now().time().minute * 60 * 60 + datetime.now().time().second + datetime.now().time().microsecond / 1000000
        m = sensor.get_sensor_value()
        output(self.P([m], []))
        while min >= m:
          min = m
          m = sensor.get_sensor_value()
          output(self.P([m], []))
        max2 = m
        m = sensor.get_sensor_value()
        output(self.P([m], []))
        while max2 <= m:
          max2 = m
          t2 = datetime.now().time().hour * 24 * 60 * 60 + datetime.now().time().minute * 60 * 60 + datetime.now().time().second + datetime.now().time().microsecond / 1000000
          m = sensor.get_sensor_value()
          output(self.P([m], []))
      if max1 >= max2:  # Check that system oscillates constantly
        break
      self.kp += step_size
    ku = self.kp
    tu = t2 - t1
    self.kp = 0.6 * ku
    self.ki = 1.2 * ku / tu
    self.kd = 0.075 * ku * tu
