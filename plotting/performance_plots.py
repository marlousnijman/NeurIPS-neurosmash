### IMPORTS ###

import matplotlib.pyplot as plt
import json
import numpy as np
import os


### CONSTANTS ###

LOG_LOCATION = os.path.join("output", "logs", "output.json")
PLOT_LOCATION = os.path.join("output", "plots")


### EXTRACTING PERFORMANCE ###

def extract_reward_data(filename):
    """ Extract reward data from json file """
    with open(filename, 'r') as openfile:
        output = json.load(openfile)

    performance = output["performance"]
    generation = []
    min_reward = []
    max_reward = []
    average_reward = []

    for gen in performance:
        generation.append(gen["generation"])
        rewards = gen["rewards"]
        min_reward.append(np.min(rewards))
        max_reward.append(np.max(rewards))
        average_reward.append(np.average(rewards))

    return generation, average_reward, min_reward, max_reward


def extract_win_data(filename):
    """ Extract win data from json file """
    with open(filename, 'r') as openfile:
        output = json.load(openfile)

    performance = output["performance"]
    generation = []
    average_wins = []

    for gen in performance:
        generation.append(gen["generation"])
        average_wins.append(np.average(gen["wins"]))

    return generation, average_wins


def extract_action_data(filename):
    """ Extract action proportion data from json file """
    with open(filename, 'r') as openfile:
        output = json.load(openfile)

    performance = output["performance"]
    generation = []
    actions = []
    action_proportions = []

    for gen in performance:
        generation.append(gen["generation"])
        actions = list(gen["actions"][0].keys()) # Get all possible actions
        gen_actions = []

        # Get all action proportions for each agent in a generation
        for i in gen["actions"]:
            gen_actions.append(list(i.values()))

        # Get mean action proportions per generation across all agents
        action_proportions.append((np.mean(gen_actions, axis=0)))

    return generation, actions, action_proportions


def extract_mutation_data(filename):
    """ Extract mutation data from json file """
    with open(filename, 'r') as openfile:
        output = json.load(openfile)

    performance = output["performance"]
    generation = []
    min_mutation_step = []
    max_mutation_step = []
    average_mutation_step = []

    for gen in performance:
        generation.append(gen["generation"])
        mutation_steps = gen["mutation_steps"]
        min_mutation_step.append(np.min(mutation_steps))
        max_mutation_step.append(np.max(mutation_steps))
        average_mutation_step.append(np.average(mutation_steps))

    return generation, average_mutation_step, min_mutation_step, max_mutation_step


### PLOTTING PERFORMANCE ###

def plot_average_rewards(reward_data):
    """ Plot average rewards across generations, including the minimal and maximal rewards per generation """
    generation, average_reward, min_reward, max_reward = reward_data
    fig, ax = plt.subplots()
    ax.plot(generation, average_reward)
    ax.fill_between(generation, min_reward, max_reward, alpha = 0.1)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Average Reward")
    ax.set_xticks(generation, generation)
    fig.savefig(os.path.join(PLOT_LOCATION, "average_rewards.png"))


def plot_cumulative_rewards(reward_data):
    """ Plot the cumulative average reward across generations """
    generation, average_reward, _, _ = reward_data
    cum_reward = np.cumsum(average_reward)
    fig, ax = plt.subplots()
    ax.plot(generation, cum_reward)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Cumulative Reward")
    ax.set_xticks(generation, generation)
    fig.savefig(os.path.join(PLOT_LOCATION, "cumulative_rewards.png"))


def plot_average_wins(win_data):
    """ Plot the average number of wins per generation """
    generation, average_wins = win_data
    fig, ax = plt.subplots()
    ax.plot(generation, average_wins)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Average #Wins")
    ax.set_xticks(generation, generation)
    fig.savefig(os.path.join(PLOT_LOCATION, "average_wins.png"))


def plot_action_proportions(action_data, agent_type=""):
    """ Plot the average action proportions per generation in a stacked bar plot """
    generation, actions, action_proportions = action_data
    action_proportions = np.asarray(action_proportions)

    fig, ax = plt.subplots()

    for i in range(action_proportions.shape[1]):
        if i == 0 :
            ax.bar(generation, action_proportions[:, i], label = f"Action {actions[i]}")
            previous_action_proportions = action_proportions[:, i]
        else:
            # stack on previous data
            ax.bar(generation, action_proportions[:, i], bottom=previous_action_proportions, label = f"Action {actions[i]}")
            previous_action_proportions += action_proportions[:, i]
            
    ax.legend()
    ax.set_xlabel("Generation")
    ax.set_ylabel("Action Proportions")
    ax.set_xticks(generation, generation)
    ax.set_ylim([0,1])
    fig.savefig(os.path.join(PLOT_LOCATION, f"action_proportions{'_' if agent_type else ''}{agent_type if agent_type else ''}.png"))


def plot_mutation_steps(mutation_data):
    """ Plot the average, minimal, and maximal mutation step per generation """
    generation, average_mutation_step, min_mutation_step, max_mutation_step = mutation_data
    fig, ax = plt.subplots()
    ax.plot(average_mutation_step, label="Mutation")
    ax.fill_between(generation, min_mutation_step, max_mutation_step, alpha = 0.1)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Average Mutation Step Size")
    ax.set_xticks(generation, generation)
    fig.savefig(os.path.join(PLOT_LOCATION, "average_mutation_step.png"))


if __name__ == "__main__":
    if not os.path.exists(PLOT_LOCATION):
        os.mkdir(PLOT_LOCATION)
    
    reward_data = extract_reward_data(LOG_LOCATION)
    win_data = extract_win_data(LOG_LOCATION)
    action_data = extract_action_data(LOG_LOCATION)
    mutation_data = extract_mutation_data(LOG_LOCATION)

    plot_average_rewards(reward_data)
    plot_cumulative_rewards(reward_data)
    plot_average_wins(win_data)
    plot_action_proportions(action_data)
    plot_mutation_steps(mutation_data)