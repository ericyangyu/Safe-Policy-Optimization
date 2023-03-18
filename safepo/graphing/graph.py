import sys;
from copy import deepcopy

from safepo.graphing.plot_rets import plot_rets_and_costs

sys.path.append('..')
import os

import numpy as np
import pandas as pd


def extract_data(path):
    """
    Extract all data from an environment
    Ex. path = "./runs/Safexp-PointGoal1-V0/"
    Return:
        data: {
            algo: {
                "seeds": (num trials)
                "time": (num trials)
                "rets": (num trials, num timesteps)
                "costs": (num trials, num timesteps)
            }
        }
    """
    data = {}
    for algo in os.listdir(path):
        data[algo] = {
            "seeds": [],
            "times": [],
            "epochs": None,
            "rets": None,
            "costs": None,
        }
        for seed in os.listdir(os.path.join(path, algo)):
            data[algo]["seeds"].append(seed)
            df = pd.read_csv(os.path.join(path, algo, seed, 'progress.txt'), sep='\s+')
            data[algo]["times"].append(df["Time"].values[-1])
            if data[algo]["epochs"] is None:
                data[algo]["epochs"] = df["Epoch"].values
            data[algo]["rets"] = df["EpRet/Mean"].values[None, :] if data[algo]["rets"] is None \
                else np.concatenate((data[algo]["rets"], df["EpRet/Mean"].values[None, :]), axis=0)
            data[algo]["costs"] = df["EpCosts/Mean"].values[None, :] if data[algo]["costs"] is None \
                else np.concatenate((data[algo]["costs"], df["EpCosts/Mean"].values[None, :]), axis=0)
    return data

if __name__ == "__main__":
    data = extract_data("./runs/Safexp-PointGoal1-V0/")

    plot_rets_and_costs(deepcopy(data))

    for algo in data:
        # Print the time taken to train each algorithm, while scaling the time by the FPS
        print(f"{algo}: {np.mean(data[algo]['times'])} +/- {np.std(data[algo]['times'])}")
