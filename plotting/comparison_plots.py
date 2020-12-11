### IMPORTS ###

from performance_plots import extract_reward_data, extract_win_data, extract_action_data, extract_mutation_data
import matplotlib.pyplot as plt
import os
import numpy as np


### CONSTANTS ###

LOG_LOCATIONS = ["output/logs/random_log.json","output/logs/dense_log.json","output/logs/random_log.json"]
#LOG_LOCATIONS = ["output/logs/random_log.json", "output/logs/dense_log.json", "output/logs/conv_log.json"]
PLOT_LOCATION = "output/plots"


### PLOTTING COMPARISONS

def plot_average_rewards_comparison(reward_data):
    fig, ax = plt.subplots()
    ax.set_xlabel("Generation")
    ax.set_ylabel("Average Reward")
    labels = ["Random", "Dense", "Convolutional"]
    for i, data in enumerate(reward_data):
        generation, average_reward, min_reward, max_reward = data
        ax.plot(generation, average_reward, label = labels[i])
        ax.fill_between(generation, min_reward, max_reward, alpha = 0.1)
        ax.set_xticks(generation, generation)
    ax.legend(loc="upper left")
    ax.grid()
    fig.savefig(os.path.join(PLOT_LOCATION, "average_rewards_comparison.png"))

def plot_cumulative_rewards_comparison(reward_data):
    fig, ax = plt.subplots()
    ax.set_xlabel("Generation")
    ax.set_ylabel("Cumulative Reward")
    labels = ["Random", "Dense", "Convolutional"]
    for i, data in enumerate(reward_data):
        generation, average_reward, _, _ = data
        cum_reward = np.cumsum(average_reward)
        ax.plot(generation, cum_reward, label = labels[i])
        ax.set_xticks(generation, generation)
    ax.legend(loc="upper left")
    ax.grid()
    fig.savefig(os.path.join(PLOT_LOCATION, "cumulative_rewards_comparison.png"))


def plot_action_proportions_comparison(action_data):
    labels = ["Random", "Dense", "Convolutional"]
    for i,data in enumerate(action_data):
        agent_type = labels[i]
        plot_action_proportions_helper(agent_type, data)

def plot_action_proportions_helper(agent_type,data):
        fig, ax = plt.subplots()
        ax.set_xlabel("Generation")
        ax.set_ylabel("Action Proportions")
        generation, actions, action_proportions = data
        action_proportions = np.asarray(action_proportions)
        for j in range(action_proportions.shape[1]):
            if j == 0 :
                ax.bar(generation, action_proportions[:, j], label = f"Action {actions[j]}")
                previous_action_proportions = action_proportions[:, j]
            else:
                # stack on previous data
                ax.bar(generation, action_proportions[:, j], bottom=previous_action_proportions, label = f"Action {actions[j]}")
                previous_action_proportions += action_proportions[:, j]
        ax.legend(loc="upper left")
        ax.grid()

        fig.savefig(os.path.join(PLOT_LOCATION, f"action_proportions_comparison_{agent_type}.png"))


def plot_mutation_steps_comparison(mutation_data):
    fig, ax = plt.subplots()
    ax.set_xlabel("Generation")
    ax.set_ylabel("Average Mutation Step Size")
    labels = ["Random", "Dense", "Convolutional"] 
    for i, data in enumerate(mutation_data):
        generation, average_mutation_step, min_mutation_step, max_mutation_step = data
        ax.plot( average_mutation_step, label=labels[i])
        ax.fill_between(generation, min_mutation_step, max_mutation_step, alpha = 0.1)
        ax.set_xticks(generation, generation)
    ax.legend(loc="upper left")
    ax.grid()
    fig.savefig(os.path.join(PLOT_LOCATION, "average_mutation_step_comparison.png"))


if __name__ == "__main__":
    reward_data = [extract_reward_data(filename) for filename in LOG_LOCATIONS]
    win_data = [extract_win_data(filename) for filename in LOG_LOCATIONS]
    action_data = [extract_action_data(filename) for filename in LOG_LOCATIONS]
    mutation_data = [extract_mutation_data(filename) for filename in LOG_LOCATIONS]

    plot_average_rewards_comparison(reward_data)
    plot_cumulative_rewards_comparison(reward_data)
    plot_action_proportions_comparison(action_data)
    plot_mutation_steps_comparison(mutation_data)