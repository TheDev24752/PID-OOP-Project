import time
from PIDController import PIDController


class PIDAutoTuning(PIDController):

  def __init__(self, setpoint):
    super().__init__(setpoint)
  
  def _ziegler_nichols(self, sensor, output, step_size, error_range): # pass through sensor object, output method, optionally step size and error
    self.kp = 1
    self.ki = 0
    self.kd = 0
    max1 = 0
    min = sensor.get_sensor_value()
    max2 = 0
    t1 = 0
    t2 = 0
    output(self.P([min], []))
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
        t1 = time.time_ns()
        m = sensor.get_sensor_value()
        output(self.P([m], []))
        while min >= m:
          min = m
          m = sensor.get_sensor_value()
          output(self.P([m], []))
        max2 = m
        m = sensor.get_sensor_value()
        output(self.P([m], []))
        time.sleep(0.05)
        while max2 <= m:
          max2 = m
          m = sensor.get_sensor_value()
          output(self.P([m], []))
        t2 = time.time_ns()
      if max2 >= max1:  # Check that system oscillates constantly
        break
      self.kp += step_size
    print(f"{t1}\r\n{t2}")
    # return (self.kp, 0.05)
    return (self.kp, (t2 - t1) / 10000000)

  def auto_tune_P(self, sensor, output, step_size = 0.1, error_range = 0.1):
    self._ziegler_nichols(sensor, output, step_size, error_range)
    self.kp /= 2
  
  def auto_tune_PI(self, sensor, output, step_size = 0.1, error_range = 0.1):
    ku, tu = self._ziegler_nichols(sensor, output, step_size, error_range)
    self.kp = 0.45 * ku
    self.ki = 0.54 * ku / tu
  
  def auto_tune_PD(self, sensor, output, step_size = 0.1, error_range = 0.1):
    ku, tu = self._ziegler_nichols(sensor, output, step_size, error_range)
    self.kp = 0.8 * ku
    self.kd = 0.1 * ku * tu
  
  def auto_tune_PID(self, sensor, output, step_size = 0.1, error_range = 0.1):
    ku, tu = self._ziegler_nichols(sensor, output, step_size, error_range)
    self.kp = 0.6 * ku
    self.ki = 1.2 * ku / tu
    self.kd = 0.075 * ku * tu
