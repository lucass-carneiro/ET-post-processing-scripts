#!/usr/bin/python3
doc="""Plot data.

Usage:
  plot.py plt <x_axis> <y_axis> <file> [--abslog] [--save=<name>] [--xlabel=<label>] [--ylabel=<label>] [--lines] [--xmin=<value>] [--xmax=<value>] [--ymin=<value>] [--ymax=<value>]
  plot.py fft <x_axis> <y_axis> <file> [--positive] [--alpha=<value>] [--smooth] [--save=<name>] [--xlabel=<label>] [--ylabel=<label>] [--lines | --linespoints] [--xmin=<value>] [--xmax=<value>] [--ymin=<value>] [--ymax=<value>]
  plot.py psd <x_axis> <y_axis> <file> [--positive] [--alpha=<value>] [--peak] [--smooth] [--save=<name>] [--xlabel=<label>] [--ylabel=<label>] [--lines | --linespoints] [--mark=<value>] [--xmin=<value>] [--xmax=<value>] [--ymin=<value>] [--ymax=<value>]
  plot.py (-h | --help)
  plot.py --version

Options:
  -h --help         Show this screen.
  --version         Show version.
  --positive        Only plot positive frequencies.
  --abslog          Plot the function in log-log scale.
  --alpha=<value>   The alpha value of the Tukey window [default: 0.0].
  --peak            Compute and print the peak of the spectrogram.
  --smooth          Apply the Savitzky - Golay smoothing filter. 
  --save=<name>     Save a figure.
  --mark=<value>    Marks a x value on the plot with a vertical line.
  --xlabel=<label>  The plot label on the x axis [default: $x$].
  --ylabel=<label>  The plot label on the y axis [default: $y$].
  --lines           Use lines instead of points to plot.
  --linespoints     Use lines and points to plot.
  --xmin=<value>    Chop the x axis to start at this value. 
  --xmax=<value>    Chop the x axis to end at this value.
  --ymin=<value>    Chop the y axis to start at this value. 
  --ymax=<value>    Chop the y axis to end at this value.

"""

from docopt import docopt

import plot_types


if __name__ ==  "__main__":
    arguments = docopt(doc, version="Plot 1.0")

    if arguments["plt"]:
        plot_types.plot(arguments)

    if arguments["fft"]:
        plot_types.fft_plot(arguments)

    if arguments["psd"]:
        assert float(arguments["--alpha"]) >= 0 and float(arguments["--alpha"]) <= 1.0, "The Tukey window alpha parameter must be in the interval (0,1)"
        plot_types.psd_plot(arguments)

