import calculus

class PIDController:
  
  def __init__():
    self.kp = 1
    self.ki = 0
    self.kd = 0
    self.setpoint = None
  
  def P(sensor_val, times):
    return self.kp * (sensor_val[-1] - self.setpoint)
  
  def PI(sensor_val, times):
    return P(sensor_val, times) + calculus.riemann(sensor_val, times)
  
  def PD(sensor_val, times):
    return P(sensor_val, times) + calculus.derivative(sensor_val[-2]. sensor_val[-1], times[-1] - times[-2])
  
  def PID(sensor_val, times):
    return PI(sensor_val, times) + calculus.derivative(sensor_val[-2]. sensor_val[-1], times[-1] - times[-2])
