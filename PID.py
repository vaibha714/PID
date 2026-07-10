"""
Built a PID control loop to simulate cruise control for a typical sedan. Calculated drag and rolling friciton to determine engine power required to maintain constant
speed. Added random error to my velocity to simulate bumps or random obstacles during a drive. Built a class for a car and the PID. Used matplotlib to graph the PID
system and the setpoint. Designed a custom GUI to allow the user to actively update the Kp, Ki, Kd, setpoint, and inital velocity. 
"""
 
import random
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class PID:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint

        self.integral = 0
        self.previous_error = 0


    def calculate(self, current_value, dt):
        error = self.setpoint - current_value 

        proportional = error * self.Kp 

        self.integral += error * dt
        integral = self.integral * self.Ki

        difference = (error - self.previous_error)/dt
        derivative = difference * self.Kd

        self.previous_error = error
        return proportional + integral + derivative
    
class Car:
    def __init__(self, drag_coefficient = .3, area = 2.2, weight = 1500):
        self.drag_coefficient = drag_coefficient
        self.area = area
        self.weight = weight

        
    def compute_speed(self, engine_power, current_velocity, dt):
        force = engine_power - (.5*1.225*(current_velocity)*abs(current_velocity)*.3*2.2) - (self.weight*9.8*.02) - random.uniform(-250,250)
        acceleration = force / self.weight

        if current_velocity + acceleration*dt > 0:
            return current_velocity + acceleration*dt
        else:
            return 0
    



def update_plant(kp,ki,kd,setpoint,velocity):

    dt = .01
    pid = PID(kp, ki, kd, setpoint)
    car = Car()
    duration = 20

    #2500, 50, 20, 55
    
    current_velocity = velocity

    history_speed = [current_velocity]

    for _ in range(int(duration/dt)):
        power = pid.calculate(current_velocity, dt)
        new_velocity = car.compute_speed(power, current_velocity, dt)

        history_speed.append(new_velocity)
        current_velocity = new_velocity

    return history_speed 



def redraw(*args):
    speed = np.array(update_plant(kp_update.get(),ki_update.get(),kd_update.get(),setpoint_update.get(),velocity_update.get()))
    time = np.arange(0,20,.01)
    line.set_data(time,speed[:-1])
    horizontal.set_ydata([setpoint_update.get(), setpoint_update.get()])
    canvas.draw()



def main():
    global line, canvas, kp_update, ki_update, kd_update, setpoint_update, horizontal, velocity_update
    
    root = tk.Tk()
    fig = Figure(figsize=(5,4), dpi =100)
    ax = fig.add_subplot()
    line, = ax.plot([], [], label = "Actual Velocity")
    horizontal = ax.axhline(0, color = "red", linestyle = "--", label = "Setpoint")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Velocity (m/s)")
    ax.grid(True)
    ax.legend(loc= "lower right")
    ax.set_ylim(0, 60)
    ax.set_xlim(0, 20)

    canvas = FigureCanvasTkAgg(fig, master=root)

    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()

    kp_update = tk.Scale(root, from_=0, to=3000, orient = tk.HORIZONTAL, command= redraw, label = "Kp")
    ki_update = tk.Scale(root, from_=0, to=100, orient = tk.HORIZONTAL, command= redraw, label = "Ki")
    kd_update = tk.Scale(root, from_=0, to=100, orient = tk.HORIZONTAL, command= redraw, label = "Kd")
    setpoint_update = tk.Scale(root, from_=0, to=55, orient = tk.HORIZONTAL, command= redraw, label = "Setpoint")
    velocity_update = tk.Scale(root, from_=0, to=30, orient=tk.HORIZONTAL, command=redraw, label = "Initial Velocity")
    button_quit = tk.Button(master=root, text = "Quit", command = root.destroy)

    kp_update.pack(side=tk.BOTTOM)
    ki_update.pack(side=tk.BOTTOM)
    kd_update.pack(side=tk.BOTTOM)
    setpoint_update.pack(side=tk.BOTTOM)
    velocity_update.pack(side=tk.BOTTOM)
    button_quit.pack(side=tk.BOTTOM)
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    kp_update.set(1500)
    ki_update.set(20)
    kd_update.set(10)
    setpoint_update.set(55)

    redraw()

    tk.mainloop()


if __name__ == "__main__":
    main()
    








