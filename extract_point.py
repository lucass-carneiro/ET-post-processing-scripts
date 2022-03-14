#!/usr/bin/env python3
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
import os

import numpy as np

from kuibit import argparse_helper as kah
from kuibit.simdir import SimDir

if __name__ == "__main__":

    desc = f"""{kah.get_program_name()} Saves a 0D value of a grid variable."""

    parser = kah.init_argparse(description=desc)
    parser.add_argument(
        "--variable",
        type=str,
        required=True,
        help="Variable to save."
    )

    parser.add_argument(
        "--type",
        type=str,
        choices=["x", "y", "z", "xy", "xz", "yz", "xyz"],
        default="xyz",
        help="Type of data (default: %(default)s)",
    )

    parser.add_argument(
        "--outname",
        type=str,
        help="Name of the output file.",
    )

    parser.add_argument(
        "-x",
        "--origin_x",
        type=float,
        help="The x value of the point to extract"
    )
    
    parser.add_argument(
        "-y",
        "--origin_y",
        type=float,
        help="The y value of the point to extract"
    )

    parser.add_argument(
        "-z",
        "--origin_z",
        type=float,
        help="The z value of the point to extract"
    )

    args = kah.get_args(parser)

    if args.outname is None:
        outname = f"{args.variable}_x_{args.origin_x}_y_{args.origin_y}_z_{args.origin_z}.npz"
    else:
        outname = args.outname

    output_path = os.path.join(args.outdir, outname)

    logger = logging.getLogger(__name__)

    if args.verbose:
        logging.basicConfig(format="%(asctime)s - %(message)s")
        logger.setLevel(logging.DEBUG)

    logger.debug(f"Reading grid function {args.variable}. This may take a while.")

    sd = SimDir(args.datadir, ignore_symlinks=args.ignore_symlinks)
    available_gfs = sd.gridfunctions[args.type]

    if not (args.variable in available_gfs):
        logger.debug(f"Grid function {args.variable} is not available. Available grid functions are: {available_gfs}")
        exit(1)

    gf = available_gfs[args.variable]

    logger.debug("Reading available iterations")
    available_iterations = gf.available_iterations
    
    logger.debug("Allocating output buffer")
    output_data = np.zeros((len(available_iterations), 3))
     
    logger.debug("Check if the user point/variable type combination is valid")
    if args.origin_x == None:
        x_is_set = False
    else:
        x_is_set = True

    if args.origin_y == None:
        y_is_set = False
    else:
        y_is_set = True

    if args.origin_z == None:
        z_is_set = False
    else:
        z_is_set = True

    if args.type == "x":
        assert x_is_set, "To extract 0D data from 1D x data, use -x <value>"
        point = (args.origin_x)
    elif args.type == "y":
        assert y_is_set, "To extract 0D data from 1D y data, use -y <value>"
        point = (args.origin_y)
    elif args.type == "z":
        assert z_is_set, "To extract 0D data from 1D z data, use -z <value>"
        point = (args.origin_z)
    elif args.type == "xy":
        assert (x_is_set and y_is_set), "To extract 0D data from 2D xy data, use -x <value> -y <value>"
        point = (args.origin_x, args.origin_y)
    elif args.type == "xz":
        assert (x_is_set and z_is_set), "To extract 0D data from 2D xz data, use -x <value> -z <value>"
        point = (args.origin_x, args.origin_z)
    elif args.type == "xz":
        assert (x_is_set and z_is_set), "To extract 0D data from 2D xz data, use -x <value> -z <value>"
        point = (args.origin_x, args.origin_z)
    elif args.type == "xyz":
        assert (x_is_set and y_is_set and z_is_set), "To extract 0D data from 3D xyz data, use -x <value> -y <value> -z <value>"
        point = (args.origin_x, args.origin_y, args.origin_z)

    logger.debug("Dumping data into output buffer. This may take a while.")
    index = 0
    for iteration in available_iterations:
        output_data[index, 0] = iteration
        output_data[index, 1] = gf.time_at_iteration(iteration)
        output_data[index, 2] = float( gf[iteration](point) )
        index += 1

    logger.debug("Serializing data. This may take a while.")
    np.save(outname, output_data)

    logger.debug("DONE.")
