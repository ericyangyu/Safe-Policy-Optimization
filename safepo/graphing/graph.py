import sys;
from copy import deepcopy

from safepo.graphing.plot_rets_and_costs import plot_rets_and_costs

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
            df = pd.read_csv(os.path.join(path, algo, seed, 'progress.txt'), sep='\s+')
            # If training is still happening, make a note and ignore
            if df['Epoch'].values.shape[0] != 500:
                print('Incomplete data, skipping. Algo: {}, Seed: {}'.format(algo, seed))
                continue

            data[algo]["seeds"].append(seed)
            data[algo]["times"].append(df["Time"].values[-1])
            if data[algo]["epochs"] is None:
                data[algo]["epochs"] = df["Epoch"].values
            data[algo]["rets"] = df["EpRet/Mean"].values[None, :] if data[algo]["rets"] is None \
                else np.concatenate((data[algo]["rets"], df["EpRet/Mean"].values[None, :]), axis=0)
            data[algo]["costs"] = df["EpCosts/Mean"].values[None, :] if data[algo]["costs"] is None \
                else np.concatenate((data[algo]["costs"], df["EpCosts/Mean"].values[None, :]), axis=0)
    return data

if __name__ == "__main__":
    for name, filename, cost, exp in [('Point Goal Env', 'point_goal_env', 25, 'Safexp-PointGoal1-V0/'), ('Point Button Env', 'point_button_env', 25, 'Safexp-PointButton1-V0/')]:
        print('Experiment: ', exp)
        data = extract_data(f"./runs/{exp}")

        import pdb; pdb.set_trace()
        plot_rets_and_costs(deepcopy(data), name, filename, cost)

        for algo in data:
            # Print how many trials it has
            print(f"{algo}: {len(data[algo]['seeds'])} trials")

            # Print the minimum time in hours taken to train each algorithm, rounded to 3 decimal places
            print(f"{algo}: {np.min(data[algo]['times']) / 3600:.3f} hours")

        print()
