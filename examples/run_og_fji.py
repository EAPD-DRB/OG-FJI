"""Run an OG-FJI baseline and an illustrative corporate-tax reform."""

import copy
import importlib.resources
import json
import multiprocessing
import os
import time

from distributed import Client
import matplotlib.pyplot as plt

from ogcore import output_plots as op
from ogcore import output_tables as ot
from ogcore.execute import runner
from ogcore.parameters import Specifications
from ogcore.utils import safe_read_pickle

plt.style.use("ogcore.OGcorePlots")


def main():
    """Solve the packaged baseline and a 25-to-20 percent CIT reform."""
    num_workers = min(multiprocessing.cpu_count(), 7)
    client = Client(
        n_workers=num_workers, processes=True, threads_per_worker=1
    )

    current_dir = os.path.dirname(os.path.realpath(__file__))
    save_dir = os.path.join(current_dir, "OG-FJI-Example")
    base_dir = os.path.join(save_dir, "OUTPUT_BASELINE")
    reform_dir = os.path.join(save_dir, "OUTPUT_REFORM")

    p = Specifications(
        baseline=True,
        num_workers=num_workers,
        baseline_dir=base_dir,
        output_base=base_dir,
    )
    defaults_path = importlib.resources.files("ogfji").joinpath(
        "ogfji_default_parameters.json"
    )
    p.update_specifications(json.loads(defaults_path.read_text()))

    start_time = time.time()
    runner(p, time_path=True, client=client)
    print("Baseline run time:", time.time() - start_time)

    p2 = copy.deepcopy(p)
    p2.baseline = False
    p2.output_base = reform_dir
    p2.update_specifications({"cit_rate": [[0.20]]})

    start_time = time.time()
    runner(p2, time_path=True, client=client)
    print("Reform run time:", time.time() - start_time)
    client.close()

    base_tpi = safe_read_pickle(os.path.join(base_dir, "TPI", "TPI_vars.pkl"))
    base_params = safe_read_pickle(os.path.join(base_dir, "model_params.pkl"))
    reform_tpi = safe_read_pickle(
        os.path.join(reform_dir, "TPI", "TPI_vars.pkl")
    )
    reform_params = safe_read_pickle(
        os.path.join(reform_dir, "model_params.pkl")
    )
    table = ot.macro_table(
        base_tpi,
        base_params,
        reform_tpi=reform_tpi,
        reform_params=reform_params,
        var_list=["Y", "C", "K", "L", "r", "w"],
        output_type="pct_diff",
        num_years=10,
        start_year=base_params.start_year,
    )
    op.plot_all(
        base_dir,
        reform_dir,
        os.path.join(save_dir, "OG-FJI_example_plots"),
    )
    table.to_csv(os.path.join(save_dir, "OG-FJI_example_output.csv"))


if __name__ == "__main__":
    main()
