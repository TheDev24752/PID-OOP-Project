class PIDController:
  
  def __init__(self, setpoint = 0):
    self.kp = 1
    self.ki = 0
    self.kd = 0
    self.setpoint = setpoint
  
  def P(self, sensor_vals, times):
    return self.kp * (sensor_vals[-1] - self.setpoint)
  
  def PI(self, sensor_vals, times):
    integral = 0
    for i in range(len(sensor_vals) - 1):
      integral += ((sensor_vals[i] - self.setpoint) + (sensor_vals[i + 1] - self.setpoint)) * (times[i] - times[i + 1]) / 2 # Area of a trapezoid
    return self.P(sensor_vals, times) + (self.ki * integral)
  
  def PD(self, sensor_vals, times):
    derivative = (sensor_vals[-1] - sensor_vals[-2]) / (times[-1] - times[-2])
    return self.P(sensor_vals, times) + (self.kd * derivative)
  
  def PID(self, sensor_vals, times):
    derivative = (sensor_vals[-1] - sensor_vals[-2]) / (times[-1] - times[-2])
    return self.PI(sensor_vals, times) + (self.kd * derivative)
