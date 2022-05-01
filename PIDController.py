import calculus

class PIDController:
  
  def __init__(self, setpoint = None):
    self.kp = 1
    self.ki = 0
    self.kd = 0
    self.setpoint = setpoint
  
  def P(self, sensor_val, times):
    return self.kp * (sensor_val[-1] - self.setpoint)
  
  def PI(self, sensor_val, times):
    return self.P(sensor_val, times) + calculus.riemann(sensor_val, times)
  
  def PD(self, sensor_val, times):
    return self.P(sensor_val, times) + calculus.derivative(sensor_val[-2]. sensor_val[-1], times[-1] - times[-2])
  
  def PID(self, sensor_val, times):
    return self.PI(sensor_val, times) + calculus.derivative(sensor_val[-2]. sensor_val[-1], times[-1] - times[-2])
