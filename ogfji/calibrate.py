"""Live demographic refresh for the OG-FJI single-industry calibration."""

import warnings

import numpy as np

from . import income

UN_COUNTRY_CODE = "242"


class Calibration:
    """Return an optional live overlay for the packaged OG-FJI defaults.

    The packaged JSON is the source of truth. With ``update_from_api=False``
    this class performs no external calls and returns only the single-industry
    identity matrices. A live update refreshes UN demographics and the
    demographics-dependent earnings matrix; documented macro and fiscal
    parameters are never overwritten.
    """

    def __init__(
        self,
        p,
        demographic_data_path=None,
        output_path=None,
        update_from_api=False,
    ):
        del output_path  # retained for compatibility with sibling models

        if p.I != 1 or p.M != 1:
            raise ValueError(
                "OG-FJI 0.1 is a single-industry calibration (I=M=1)."
            )

        self.demographic_params = {}
        self.e = None
        self.alpha_c = np.array([1.0])
        self.io_matrix = np.array([[1.0]])

        if not update_from_api:
            return

        try:
            from ogcore import demographics

            self.demographic_params = demographics.get_pop_objs(
                p.E,
                p.S,
                p.T,
                0,
                99,
                country_id=UN_COUNTRY_CODE,
                initial_data_year=p.start_year - 1,
                final_data_year=p.start_year + 1,
                GraphDiag=False,
                download_path=demographic_data_path,
            )
            demog80 = demographics.get_pop_objs(
                20,
                80,
                p.T,
                0,
                99,
                country_id=UN_COUNTRY_CODE,
                initial_data_year=p.start_year - 1,
                final_data_year=p.start_year + 1,
                GraphDiag=False,
            )
            self.e = income.get_e_interp(
                p.E,
                p.S,
                p.J,
                p.lambdas,
                demog80["omega_SS"],
            )
        except Exception as exc:
            warnings.warn(
                f"Demographics/income update failed: {exc}", stacklevel=2
            )
            self.demographic_params = {}
            self.e = None

    def get_dict(self):
        """Return parameters that should overlay the packaged defaults."""
        result = dict(self.demographic_params)
        if self.e is not None:
            result["e"] = self.e
        result["alpha_c"] = self.alpha_c
        result["io_matrix"] = self.io_matrix
        return result
