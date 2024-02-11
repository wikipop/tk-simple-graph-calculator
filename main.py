from tkinter import *
from tkinter import ttk
import numpy as np

root = Tk()
graph = ttk.Frame(root, padding=10)
options = ttk.Frame(root, padding=10)
graph.grid(column=0, row=0)
options.grid(column=1, row=0)

canvas = Canvas(graph, bg='white', width=1280, height=720)
canvas.grid(column=0, row=0)

function_frame = ttk.Frame(options, padding=10)
function_frame.grid(column=0, row=0)
ttk.Label(function_frame, text='Function:').grid(column=0, row=0)
function_box = ttk.Entry(function_frame)
function_box.grid(column=0, row=1)
function_box.insert(0, 'x**2')

accuracy_frame = ttk.Frame(options, padding=10)
accuracy_frame.grid(column=0, row=1)
ttk.Label(accuracy_frame, text='Accuracy (ε):').grid(column=0, row=0)
accuracy_box = ttk.Entry(accuracy_frame)
accuracy_box.grid(column=1, row=0)
accuracy_box.insert(0, '1')

scale_frame = ttk.Frame(options, padding=10)
scale_frame.grid(column=0, row=2)
ttk.Label(scale_frame, text='Scale:').grid(column=0, row=0)
scale_box = Scale(scale_frame, from_=1, to=100, orient=HORIZONTAL)
scale_box.grid(column=1, row=0)


def draw_point(x, y):
    x = int(x)
    y = int(y)
    canvas.create_oval(x, y, x + 1, y + 1, fill='black')


def draw_line(x1, y1, x2, y2):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    canvas.create_line(x1, y1, x2, y2, fill='black')


def evaluate_function(function, accuracy, max_x: int, max_y: int) -> [(float, float)]:
    plot_data = []

    x = np.arange(-max_x, max_x, accuracy)
    try:
        y = eval(function, {'x': x})
    except Exception as e:
        ttk.Label(function_frame, text='Invalid function')
        return plot_data

    ttk.Label(function_frame, text='Function:')

    for i in range(len(x)):
        plot_data.append((x[i], y[i]))

    return plot_data


def loop():
    canvas.delete("all")
    print('frame updated')

    w_width = canvas.winfo_reqwidth()
    w_height = canvas.winfo_reqheight()

    function_value = function_box.get()

    if accuracy_box.get().isnumeric() and float(accuracy_box.get()) > 0.0001:
        accuracy = float(accuracy_box.get())
    else:
        accuracy = 1

    scale = scale_box.get()

    plot_values = evaluate_function(function_value, accuracy, w_width // 2, w_height // 2)

    if plot_values:
        last_value = plot_values[0]
        for i in plot_values[1:]:
            draw_line(last_value[0] * scale + w_width / 2, -last_value[1] * scale + w_height / 2,
                      i[0] * scale + w_width / 2,
                      -i[1] * scale + w_height / 2)

            last_value = i

    # TODO: Think of a function to generate scale numbers
    scale_numbers = []

    for number in scale_numbers:
        draw_line(w_width / 2 - w_width / 60, -number * scale + w_height / 2, w_width / 2 + w_width / 60,
                  -number * scale + w_height / 2)
        canvas.create_text(w_width / 2 + w_width / 60, -number * scale + w_height / 2, text=str(number), fill='black')

    canvas.create_line(w_width / 2, 0, w_width / 2, w_height, fill='black')
    canvas.create_line(0, w_height / 2, w_width, w_height / 2, fill='black')

    canvas.create_text(w_width / 2 + w_width / 60, w_height / 2 + w_height / 60, text='(0, 0)', fill='black')
    canvas.create_text(w_width - w_width / 60, w_height / 2 + w_height / 60, text='x', fill='black')
    canvas.create_text(w_width / 2 + w_width / 60, w_height / 60, text='y', fill='black')

    root.after(500, loop)


root.after(10, loop)
root.mainloop()
