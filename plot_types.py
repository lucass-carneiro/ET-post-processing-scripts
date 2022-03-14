import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import savgol_filter

def plot(arguments):
    x_axis = int(arguments["<x_axis>"])
    y_axis = int(arguments["<y_axis>"])

    x_label = arguments["--xlabel"]
    y_label = arguments["--ylabel"]

    file_path = arguments["<file>"]
    file_extension = os.path.splitext(file_path)[1]
    
    save = arguments["--save"]

    if arguments["--lines"]:
        style = "-"
    else:
        style = "o"

    if file_extension == ".npy" or file_extension == ".npz":
        data = np.load(file_path)
        xData = data[:, x_axis]
        yData = data[:, y_axis]
    else:
        data = np.loadtxt(file_path, usecols=[x_axis, y_axis])
        xData = data[:, 0]
        yData = data[:, 1]

    font_size = 30
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['font.family'] = 'Latin Modern Roman'
    plt.rcParams['figure.figsize'] = [10, 8]

    plt.close('all')

    if arguments["--abslog"]:
        plt.plot(xData, np.abs(yData), style, color='black')
        plt.yscale("log")
    else:
        plt.plot(xData, yData, style, color='black')

    current_xmin, current_xmax = plt.xlim()
    current_ymin, current_ymax = plt.ylim()
    
    if arguments["--xmin"] != None:
        current_xmin = float(arguments["--xmin"])
   
    if arguments["--xmax"] != None:
        current_xmax = float(arguments["--xmax"])
    
    if arguments["--ymin"] != None:
        current_ymin = float(arguments["--ymin"])
    
    if arguments["--ymax"] != None:
        current_ymax = float(arguments["--ymax"])
    
    plt.xlim(current_xmin, current_xmax)
    plt.ylim(current_ymin, current_ymax)

    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel(y_label, fontsize=font_size)

    plt.tick_params(axis='both', which='major', labelsize=font_size)

    if save != None:
        plt.tight_layout()
        plt.savefig(save)
    else:
        plt.show()

def fft_plot(arguments):
    x_axis = int(arguments["<x_axis>"])
    y_axis = int(arguments["<y_axis>"])

    x_label = arguments["--xlabel"]
    y_label = arguments["--ylabel"]

    file_path = arguments["<file>"]
    file_extension = os.path.splitext(file_path)[1]
    
    save = arguments["--save"]

    if not arguments["--lines"] and not arguments["--linespoints"]:
        style = "o"
    else:
        style = "-"

    if file_extension == ".npy" or file_extension == ".npz":
        data = np.load(file_path)
        xData = data[:, x_axis]
        yData = data[:, y_axis]
    else:
        data = np.loadtxt(file_path, usecols=[x_axis, y_axis])
        xData = data[:, 0]
        yData = data[:, 1]

    # Time step and sampling frequencies
    dt = xData[1] - xData[0]
    fs = 1/dt
   
    # Window and trasforms
    W = signal.windows.tukey(len(xData), alpha=float(arguments["--alpha"]), sym=True)
    yBar = np.fft.fft(yData * W)/fs
    f = np.fft.fftfreq(len(xData), dt)

    yBar = np.fft.fftshift(yBar)
    f = np.fft.fftshift(f)

    if arguments["--positive"]:
        f_positive = (f > 0)
        f = f[f_positive]
        yBar = yBar[f_positive]

    font_size = 30
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['font.family'] = 'Latin Modern Roman'
    plt.rcParams['figure.figsize'] = [10, 8]

    plt.close('all')
    plt.plot(f, np.abs(yBar), style, color='black')

    if arguments["--linespoints"]:
        plt.plot(f, np.abs(yBar), "o", color='black')

    current_xmin, current_xmax = plt.xlim()
    current_ymin, current_ymax = plt.ylim()
    
    if arguments["--xmin"] != None:
        current_xmin = float(arguments["--xmin"])
   
    if arguments["--xmax"] != None:
        current_xmax = float(arguments["--xmax"])
    
    if arguments["--ymin"] != None:
        current_ymin = float(arguments["--ymin"])
    
    if arguments["--ymax"] != None:
        current_ymax = float(arguments["--ymax"])
    
    plt.xlim(current_xmin, current_xmax)
    plt.ylim(current_ymin, current_ymax)

    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel(y_label, fontsize=font_size)

    plt.tick_params(axis='both', which='major', labelsize=font_size)

    if save != None:
        plt.tight_layout()
        plt.savefig(save)
    else:
        plt.show()

def psd_plot(arguments):
    x_axis = int(arguments["<x_axis>"])
    y_axis = int(arguments["<y_axis>"])

    x_label = arguments["--xlabel"]
    y_label = arguments["--ylabel"]

    file_path = arguments["<file>"]
    file_extension = os.path.splitext(file_path)[1]
    
    save = arguments["--save"]

    if not arguments["--lines"] and not arguments["--linespoints"]:
        style = "o"
    else:
        style = "-"

    if file_extension == ".npy" or file_extension == ".npz":
        data = np.load(file_path)
        xData = data[:, x_axis]
        yData = data[:, y_axis]
    else:
        data = np.loadtxt(file_path, usecols=[x_axis, y_axis])
        xData = data[:, 0]
        yData = data[:, 1]

    # Time step
    dt = xData[1] - xData[0]
    
    # Transforms and window
    W = signal.windows.tukey(len(xData), alpha=float(arguments["--alpha"]), sym=True)
    yBar = np.fft.fft(yData * W)
    f = np.fft.fftfreq(len(xData), dt)

    yBar = np.fft.fftshift(yBar)
    f = np.fft.fftshift(f)

    S = np.sum(W**2)
    PSD = dt/S * np.abs(yBar)**2

    if arguments["--positive"]:
        f_positive = (f >= 0.0)
        f = f[f_positive]
        PSD = PSD[f_positive]
        PSD = 2 * PSD
       
    if arguments["--peak"]:
        peak_val = np.amax(PSD)
        peak_index = np.where(PSD == peak_val)
        print("Peak values: ", end="")
        print(peak_val)
        print("Peak frequencies: ", end="")
        print(f[peak_index] * 2.0 * np.pi)
        print(f[(peak_index[0][0] + 1)] * 2.0 * np.pi)
        print(f[(peak_index[0][0] - 1)] * 2.0 * np.pi)

    if arguments["--smooth"] and arguments["--lines"]:
        PSD = savgol_filter(PSD, 21, 3)

    font_size = 30
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['font.family'] = 'Latin Modern Roman'
    plt.rcParams['figure.figsize'] = [10, 8]

    plt.close('all')
    plt.plot(f, PSD, style, color='black')

    if arguments["--linespoints"]:
        plt.plot(f, PSD, "o", color='black')

    current_xmin, current_xmax = plt.xlim()
    current_ymin, current_ymax = plt.ylim()
    
    if arguments["--xmin"] != None:
        current_xmin = float(arguments["--xmin"])
   
    if arguments["--xmax"] != None:
        current_xmax = float(arguments["--xmax"])
    
    if arguments["--ymin"] != None:
        current_ymin = float(arguments["--ymin"])
    
    if arguments["--ymax"] != None:
        current_ymax = float(arguments["--ymax"])

    if arguments["--mark"] != None:
        plt.axvline(float(arguments["--mark"]), 0, 0.98, color="red", label="$x = %f$" % float(arguments["--mark"]))
        plt.legend()
    
    plt.xlim(current_xmin, current_xmax)
    plt.ylim(current_ymin, current_ymax)

    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel(y_label, fontsize=font_size)

    plt.tick_params(axis='both', which='major', labelsize=font_size)

    if save != None:
        plt.tight_layout()
        plt.savefig(save)
    else:
        plt.show()
