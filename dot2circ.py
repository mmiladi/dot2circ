#!/usr/bin/env python

import argparse
from subprocess import call
from subprocess import check_output

DESCRIPTION = """
dot2circ - convert ViennaRNA dotplots to circular base-pairing diagrams

Given an RNA sequence, calculate base-pairing probabilities with RNAplfold and
plot them using circos.
"""

EPILOG = """
Status: rickety prototype.

fixed relative paths, has to be called from program directory.
no checking for valid parameters.
no checking if required software is available.
folding temperature set to 25C.
folding parameters set to W150 L100.
color annotation set to my current test sequence.
"""

RNAPLFOLD_PARAMS = "-W 150 -L 100 "
RNAFOLD_PARAMS = ""

PERLBIN = ""
CIRCOSBIN = "circos"

# parse command line arguments
parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
parser.add_argument(
    "sequence",
    help="input RNA sequence")
parser.add_argument(
    "--prefix",
    default="dot2circ",
    help="prefix of output files")
parser.add_argument("--local-fold",
                    type=bool,
                    default = False,
                    help="compute local dotplot using RNAplFold")
parser.add_argument("--temperature",
                    type=int,
                    default = 37,
                    help="folding temperature")


args = parser.parse_args()

# fold
if args.local_fold is True:
    foldcmd = 'echo {0} | RNAplfold {1} '.format(args.sequence, RNAPLFOLD_PARAMS)
else:
    foldcmd = 'echo {0} | RNAfold -p '.format(args.sequence)

foldcmd += '-T {}'.format(args.temperature)

    
foldout = check_output(foldcmd, shell=True)


# create circos data
if args.local_fold is True:
    call(['./parse_plfold.sh'], shell=True)
else:
    call(['./parse_rnafold.sh'], shell=True)

# run circos
circoscmd = '{0} {1} -param image/file**="{2}.png" '.format(
    PERLBIN,
    CIRCOSBIN,
    args.prefix)
circoscmd += "" 
#"""\
#-param links/link/rules/annot1_1st_stem_start=139 \
#  -param links/link/rules/annot1_1st_stem_end=157 \
#-param links/link/rules/annot1_2nd_stem_start=181 \
#  -param links/link/rules/annot1_2nd_stem_end=206 \
#-param links/link/rules/annot2_1st_stem_start=179 \
#  -param links/link/rules/annot2_1st_stem_end=198 \
#-param links/link/rules/annot2_2nd_stem_start=227 \
#  -param links/link/rules/annot2_2nd_stem_end=246"""
print 'calling: "{0}"'.format(circoscmd)
circosout = check_output(circoscmd, shell=True)
