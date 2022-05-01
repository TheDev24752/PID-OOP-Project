class PIDController:
  
  def __init__(self, setpoint = None):
    self.kp = 1
    self.ki = 0
    self.kd = 0
    self.setpoint = setpoint
  
  def P(self, sensor_val, times):
    return self.kp * (sensor_val[-1] - self.setpoint)
  
  def PI(self, sensor_val, times):
    integral = 0
    for i in range(len(sensor_val) - 1):
      integral += ((sensor_val[i] - self.setpoint) + (sensor_val[i + 1] - self.setpoint)) * (times[i] - times[i + 1]) / 2 # Area of a trapezoid
    return self.P(sensor_val, times) + integral
  
  def PD(self, sensor_val, times):
    derivative = (sensor_val[-1] - sensor_val[-2]) / (times[-1] - times[-2])
    return self.P(sensor_val, times) + derivative
  
  def PID(self, sensor_val, times):
    derivative = (sensor_val[-1] - sensor_val[-2]) / (times[-1] - times[-2])
    return self.PI(sensor_val, times) + derivative
