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

from datetime import datetime

from kuibit import argparse_helper as kah
from kuibit.simdir import SimDir

import numpy as np

if __name__ == "__main__":
    desc = f"""\
{kah.get_program_name()} Saves the multipolar decomposition of the Klein-Gordon
Scalar field as measured by a given radius and at a given l and m."""

    parser = kah.init_argparse(desc)

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

    filename = f"{args.name}_{args.mult_l}{args.mult_m}_r{args.radius}_" + datetime.now().strftime("%d_%m_%Y_%H:%M:%S") + ".ascii"
    
    logger.debug(f"Using file name {filename}")

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

    logger.debug("Saving")

    phi.save(filename)
        
    logger.debug("DONE")

