from datetime import datetime
from PIDController import PIDController


class PIDAutoTuning(PIDController):

  def __init__(self, setpoint):
    super().__init__(setpoint)
  
  def _ziegler_nichols(self, sensor, output, step_size, error_range):
    self.kp = 1
    self.ki = 0
    self.kd = 0
    max1 = sensor.get_sensor_value()
    min = 0
    max2 = 0
    t1 = 0
    t2 = 0
    output(self.P([sensor.get_sensor_value()], []))
    while True:
      for i in range(3): # run system for 3 periods, so that it can settle into oscillation
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
    return (self.kp, t2 - t1)
  
  def tune_P(self, sensor, output, step_size = 0.1, error_range = 0.1): # pass through sensor object, output method, optionally step size and error
    self._ziegler_nichols(sensor, output, step_size, error_range)
    self.kp /= 2.0
  
  def ziegler_nichols_PI(self, sensor, output, step_size = 0.1, error_range = 0.1): # pass through sensor object, output method, optionally step size and error
    ku, tu = self._ziegler_nichols(sensor, output, step_size, error_range)
    self.kp = 0.45 * ku
    self.ki = 0.54 * ku / tu
  
  def ziegler_nichols_PD(self, sensor, output, step_size = 0.1, error_range = 0.1): # pass through sensor object, output method, optionally step size and error
    ku, tu = self._ziegler_nichols(sensor, output, step_size, error_range)
    self.kp = 0.8 * ku
    self.kd = 0.1 * ku * tu
  
  def ziegler_nichols_PID(self, sensor, output, step_size = 0.1, error_range = 0.1): # pass through sensor object, output method, optionally step size and error
    ku, tu = self._ziegler_nichols(sensor, output, step_size, error_range)
    self.kp = 0.6 * ku
    self.ki = 1.2 * ku / tu
    self.kd = 0.075 * ku * tu
