#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK

# Copyright (C) 2020-2021 Gabriele Bozzola
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, see <https://www.gnu.org/licenses/>.

import logging

import matplotlib as mpl
import matplotlib.pyplot as plt

from kuibit import argparse_helper as kah
from kuibit.simdir import SimDir
from kuibit.visualize_matplotlib import (
    add_text_to_corner,
    get_figname,
    save_from_dir_filename_ext,
    set_axis_limits_from_args,
    setup_matplotlib,
)

import numpy as np

if __name__ == "__main__":
    setup_matplotlib()

    desc = f"""\
{kah.get_program_name()} Plots the multipolar decomposition of the Klein-Gordon
Scalar field as measured by a given radius and at a given l and m."""

    parser = kah.init_argparse(desc)
    kah.add_figure_to_parser(parser, add_limits=True)

    parser.add_argument(
        "--save",
        dest="save_fig",
        action="store_true",
        help="Should the figure be saved or shown? Default: False (only shown)"
    )
    parser.set_defaults(save_fig=False)

    parser.add_argument(
        "--log-abs",
        dest="plot_log_of_abs",
        action="store_true",
        help="Should we plot the function or the log of it's absolute value? Default: False"
    )
    parser.set_defaults(plot_log_of_abs=False)

    parser.add_argument(
        "--font-size",
        type=int,
        default=20,
        help="Base font size for the plots. Default: 20"
    )

    parser.add_argument(
        "--name",
        type=str,
        default="phi",
        help="The actual name of the multipole grid function."
    )

    parser.add_argument(
        "--radius",
        type=float,
        required=True,
        help="Radius of the multipole extraction."
    )

    parser.add_argument(
        "--mult-l",
        type=int,
        default=0,
        help="Multipole number l."
    )
    parser.add_argument(
        "--mult-m",
        type=int,
        default=0,
        help="Multipole number m."
    )

    args = kah.get_args(parser)

    # Parse arguments

    logger = logging.getLogger(__name__)

    if args.verbose:
        logging.basicConfig(format="%(asctime)s - %(message)s")
        logger.setLevel(logging.DEBUG)

    figname = get_figname(
        args,
        default=f"{args.name}_{args.mult_l}{args.mult_m}_r{args.radius}",
    )
    logger.debug(f"Using figname {figname}")

    sim = SimDir(args.datadir, ignore_symlinks=args.ignore_symlinks)

    logger.debug("Prepared SimDir")

    reader_mult = sim.multipoles

    if args.name not in reader_mult:
        raise ValueError(f"{args.name} not available")

    reader = reader_mult[args.name]

    logger.debug(f"Using radius: {args.radius}")

    av_radii = reader.radii

    if args.radius not in av_radii:
        logger.debug(f"Available radii {av_radii}")
        raise ValueError(f"{args.radii} not available")

    detector = reader[args.radius]

    if (args.mult_l, args.mult_m) not in detector.available_lm:
        logger.debug(f"Available multipoles {detector.available_lm}")
        raise ValueError(f"Multipole {args.mult_l}, {args.mult_m} not available")

    phi = detector[args.mult_l, args.mult_m]

    logger.debug(f"Plotting {args.name}")

    font_size = args.font_size

    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['font.family'] = 'Latin Modern Roman'
    plt.rcParams['figure.figsize'] = [10, 8]

    plt.title(fr"Klein-Gordon $\Phi({args.radius:.3f}, t)$ Multipole", fontsize = font_size)

    plt.xlabel(r"$t$", fontsize = font_size)

    plt.tick_params(axis="both", which="major", labelsize=font_size)

    if args.plot_log_of_abs:
        plt.plot(np.log(phi.abs()), color="black")        
        plt.ylabel(fr"$\left| \Phi_{{{args.mult_l}{args.mult_m}}}(r,t) \right|$", fontsize = font_size)
    else:
        plt.plot(
            phi.real(),
            color="black",
            label=fr"$\Re \left( \Phi_{{{args.mult_l}{args.mult_m}}} \right)$"
        )
        
        plt.plot(
            phi.imag(),
            color="red",
            label=fr"$\Im \left( \Phi_{{{args.mult_l}{args.mult_m}}} \right)$",
        )

        plt.ylabel(fr"$\Phi_{{{args.mult_l}{args.mult_m}}}(r,t)$", fontsize = font_size)

        plt.legend()

    set_axis_limits_from_args(args)
    plt.tight_layout()

    logger.debug("Plotted")

    if args.save_fig:
      logger.debug("Saving")
      save_from_dir_filename_ext(
          args.outdir,
          figname,
          args.fig_extension
      )
    else:
        logger.debug("Showing plot")
        plt.show()
        
    logger.debug("DONE")

