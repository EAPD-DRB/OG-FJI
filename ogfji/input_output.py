import pandas as pd
import numpy as np
import os
from ogfji.constants import CONS_DICT, PROD_DICT

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

# Social Accounting Matrix (SAM) file for Fiji.
#
# NOT YET SOURCED. OG-FJI currently runs single-industry (M=1, I=1), which
# needs no SAM: ogfji.calibrate only calls the functions below when M > 1 or
# I > 1. Everything in this module is machinery waiting on data.
#
# To enable a multi-industry OG-FJI, source a SAM or supply-and-use table, ship
# it in ogfji/data/, and set SAM_FILENAME to its name. Search in this order:
#   1. Fiji Bureau of Statistics -- national supply-and-use / input-output
#      tables. These are sufficient; the make/use algebra runs on them
#      directly.
#   2. Institute-built country SAMs -- UNU-WIDER's country SAM programme and
#      IFPRI's Nexus country-SAM collection, both free and documented.
#   3. Global harmonised databases (GTAP, EORA, OECD ICIO) as a last resort,
#      marked lower-confidence: their balancing steps go beyond the national
#      accounts and most lack the household and factor detail a SAM carries.
#
# Match the SAM's vintage to the labour force survey year used for employment,
# and confirm it reproduces Fiji Bureau of Statistics GDP-by-industry shares
# before reading anything off it. Mirror the file in EAPD-DRB/SAM-files or ship
# a compact extract here -- never read a publisher URL at runtime.
SAM_FILENAME = None


def read_SAM():
    """
    Read in the packaged Social Accounting Matrix (SAM) file.

    Returns:
        SAM (pd.DataFrame | None): Social Accounting Matrix, or None
            if unavailable
    """
    if SAM_FILENAME is None:
        print(
            "No SAM has been sourced for Fiji yet, so multi-industry "
            "calibration is unavailable. Single-industry OG-FJI (M=1, I=1) "
            "does not need one. See the note on SAM_FILENAME in "
            "ogfji/input_output.py."
        )
        return None
    try:
        sam = pd.read_csv(
            os.path.join(CUR_DIR, "data", SAM_FILENAME),
            index_col=1,
            thousands=",",
        )
        sam.fillna(0, inplace=True)
        return sam
    except Exception as exc:
        print(f"Failed to read packaged SAM file: {exc}")
        return None


def get_alpha_c(sam=None, cons_dict=CONS_DICT):
    """
    Calibrate the alpha_c vector, showing the shares of household
    expenditures for each consumption category

    Args:
        sam (pd.DataFrame): SAM file
        cons_dict (dict): Dictionary of consumption categories

    Returns:
        alpha_c (dict): Dictionary of shares of household expenditures
    """
    if sam is None:
        sam = read_SAM()
    if sam is None:
        raise RuntimeError("SAM data is unavailable. Cannot compute alpha_c.")
    hh_cols = [
        "hhd-r1",
        "hhd-r2",
        "hhd-r3",
        "hhd-r4",
        "hhd-r5",
        "hhd-u1",
        "hhd-u2",
        "hhd-u3",
        "hhd-u4",
        "hhd-u5",
    ]
    alpha_c = {}
    overall_sum = 0
    for key, value in cons_dict.items():
        # note the subtraction of the row to focus on domestic consumption
        category_total = (
            sam.loc[sam.index.isin(value), hh_cols].values.astype(float).sum()
        )
        alpha_c[key] = category_total
        overall_sum += category_total
    for key, value in cons_dict.items():
        alpha_c[key] = alpha_c[key] / overall_sum

    return alpha_c


def get_io_matrix(sam=None, cons_dict=CONS_DICT, prod_dict=PROD_DICT):
    """
    Calibrate the io_matrix array.  This array relates the share of each
    production category in each consumption category

    Args:
        sam (pd.DataFrame): SAM file
        cons_dict (dict): Dictionary of consumption categories
        prod_dict (dict): Dictionary of production categories

    Returns:
        io_df (pd.DataFrame): Dataframe of io_matrix
    """
    if sam is None:
        sam = read_SAM()
    if sam is None:
        raise RuntimeError(
            "SAM data is unavailable. Cannot compute io_matrix."
        )
    # Create initial matrix as dataframe of 0's to fill in
    io_dict = {}
    for key in prod_dict.keys():
        io_dict[key] = np.zeros(len(cons_dict.keys()))
    io_df = pd.DataFrame(io_dict, index=cons_dict.keys())
    # Fill in the matrix
    # Note, each cell in the SAM represents a payment from the columns
    # account to the row account
    # (see https://www.un.org/en/development/desa/policy/capacity/presentations/manila/6_sam_mams_fiji.pdf)
    # We are thus going to take the consumption categories from rows and
    # the production categories from columns
    for ck, cv in cons_dict.items():
        for pk, pv in prod_dict.items():
            io_df.loc[io_df.index == ck, pk] = (
                sam.loc[sam.index.isin(cv), pv].values.astype(float).sum()
            )
    # change from levels to share (where each row sums to one)
    io_df = io_df.div(io_df.sum(axis=1), axis=0)

    return io_df
