import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as Animation
from tkinter import *
from tkinter import ttk
import time
from PID_Auto_Tuning import PIDAutoTuning
from SensorInput import SensorInput

# define globals
graph_y = 0
setpoint = 100
velocity = 0

inputs = []
times = []


def noise():
    comp_proportional = -10
    comp_static = (time.time_ns() * 7 + 13) % 11

    return (comp_static + comp_proportional) / 10


def change_vel(change):
    global velocity, graph_y
    velocity -= change * 0.01
    graph_y += velocity


def get_sensor_value():
    global graph_y
    return graph_y


def change_set_point():
    global setpoint, set_point_box, current_set_point, inputs, times
    try:
        # attempt to get the new setpoint
        new_point = set_point_box.get('1.0', 'end')
        new_point = float(new_point)
    except ValueError:
        set_point_box.delete('1.0', 'end')
        set_point_box.insert('end', "err")
        return

    times = times[-2:]
    inputs = inputs[-2:]

    setpoint = new_point
    new_point = f"{setpoint:.3f}"
    set_point_box.delete('1.0', 'end')
    set_point_box.insert('end', f"{new_point}")
    current_set_point.config(text=f"PID set-point: {setpoint:.3f}")


def update():
    global graph_y, controller, setpoint
    # all the code that controls the PID, Sensor, and other shenanigans that update every cycle go here
    graph_y += noise()
    inputs.append(graph_y)
    times.append(time.process_time_ns() / (10**9))
    controller.setpoint = setpoint
    if len(inputs) > 1:
        change_vel(controller.PID(inputs, times))
    return


def animate_graph(i):
    # simulate!
    update()

    # limit-ate!
    x_vals = []
    y_vals = []

    if len(inputs) < 100:
        x_vals = times
        y_vals = [i % 360 for i in inputs]
    else:
        # get the 100 most recent samples
        x_vals = times[-100:]
        y_vals = [i % 360 for i in inputs[-100:]]

    # display-te!
    graph.clear()
    graph.plot(x_vals, y_vals)
    graph.set_ylim([0, 360])


sensor = SensorInput(get_sensor_value)
controller = PIDAutoTuning(setpoint)

controller.auto_tune_PID(sensor, change_vel)

# region create window
root = Tk()
root.title('PID Simulation')
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Sensor output").grid(column=0, row=0)
# endregion

# region create graph
fig = Figure(figsize=(5, 5), dpi=75)
graph = fig.add_subplot(111)
graph.set_title("heading vs time")

canvas = FigureCanvasTkAgg(fig, frm)
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=2)
# endregion

# region create set-point text
current_set_point = ttk.Label(frm, text=f"PID set-point: {setpoint:.3f}")
current_set_point.grid(column=0, row=3)

new_set_point = ttk.Label(frm, text="Set new set-point:")
new_set_point.grid(column=0, row=4)

set_point_box = Text(frm, height=1, width=8)
set_point_box.insert('end', "0.000")
set_point_box.grid(column=1, row=4)
# endregion

# region create buttons
ttk.Button(frm, text="Update set-point", command=change_set_point).grid(column=0, row=5)

ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=5)
# endregion

ani = Animation.FuncAnimation(fig, animate_graph, interval=50)
root.mainloop()
