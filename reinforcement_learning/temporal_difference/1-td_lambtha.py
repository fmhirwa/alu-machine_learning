#!/usr/bin/env python3
import numpy as np

def td_lambtha(env, V, policy, lambtha, episodes=5000, max_steps=100, alpha=0.1, gamma=0.99):
    """
    Performs the TD(λ) algorithm using accumulating eligibility traces to update the state-value function V.

    Args:
        env: OpenAI Gym environment instance.
        V (np.ndarray): Array of shape (s,) containing the value estimates.
        policy (function): A function that takes in a state and returns an action.
        lambtha (float): The eligibility trace decay factor.
        episodes (int): Total number of episodes to train over.
        max_steps (int): Maximum number of steps per episode.
        alpha (float): Learning rate.
        gamma (float): Discount factor.

    Returns:
        np.ndarray: The updated value estimate V.
    """
    for _ in range(episodes):
        state = env.reset()
        # Initialize eligibility trace vector for all states
        e = np.zeros_like(V)
        for _ in range(max_steps):
            action = policy(state)
            next_state, reward, done, _ = env.step(action)
            # TD error: reward + gamma * V(next_state) - V(state)
            td_error = reward + gamma * V[next_state] - V[state]
            # Increment eligibility trace for the current state (accumulating trace)
            e[state] += 1
            # Update value estimates for all states
            V += alpha * td_error * e
            # Decay eligibility traces for all states
            e *= gamma * lambtha
            state = next_state
            if done:
                break
    return V
