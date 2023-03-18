import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_rets_and_costs(data):
    """
    Plot the average (with variance) returns and costs of all data
    """
    sns.set()
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    for algo in data:
        # Smooth the data first
        for i in range(data[algo]["rets"].shape[0]):
            data[algo]["rets"][i, :] = pd.Series(data[algo]["rets"][i, :]).rolling(10).mean().values
            data[algo]["costs"][i, :] = pd.Series(data[algo]["costs"][i, :]).rolling(10).mean().values


        ax[0].plot(data[algo]["epochs"], data[algo]["rets"].mean(axis=0), label=algo, linewidth=2)
        ax[0].fill_between(data[algo]["epochs"], data[algo]["rets"].mean(axis=0) - data[algo]["rets"].std(axis=0),
                           data[algo]["rets"].mean(axis=0) + data[algo]["rets"].std(axis=0), alpha=0.3)
        ax[1].plot(data[algo]["epochs"], data[algo]["costs"].mean(axis=0), label=algo, linewidth=2)
        ax[1].fill_between(data[algo]["epochs"], data[algo]["costs"].mean(axis=0) - data[algo]["costs"].std(axis=0),
                           data[algo]["costs"].mean(axis=0) + data[algo]["costs"].std(axis=0), alpha=0.3)
    ax[0].set_title("Point Goal Env Returns")
    ax[0].set_xlabel("Epoch")
    ax[0].set_ylabel("Average Return")
    ax[1].set_title("Point Goal Env Costs")
    ax[1].set_xlabel("Epoch")
    ax[1].set_ylabel("Average Cost")
    ax[-1].legend()
    plt.savefig("./graphing/images/point_goal_env.png")
    plt.close()




    # sns.set()
    # plt.figure(figsize=(8, 6))
    # for algo in data:
    #     plt.plot(data[algo]["epochs"], data[algo]["rets"].mean(axis=0), label=algo, linewidth=2)
    #     plt.fill_between(data[algo]["epochs"], data[algo]["rets"].mean(axis=0) - data[algo]["rets"].std(axis=0),
    #                      data[algo]["rets"].mean(axis=0) + data[algo]["rets"].std(axis=0), alpha=0.3)
    # plt.legend()
    # plt.title("Point Goal Env Returns")
    # plt.xlabel("Epoch")
    # plt.ylabel("Average Return")
    # plt.show()