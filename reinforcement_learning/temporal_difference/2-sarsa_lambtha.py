#!/usr/bin/env python3
import numpy as np

def sarsa_lambtha(env, Q, lambtha, episodes=5000, max_steps=100,
                  alpha=0.1, gamma=0.99, epsilon=1, min_epsilon=0.1,
                  epsilon_decay=0.05):
    """
    Performs the SARSA(λ) algorithm with eligibility traces to update the action-value function Q.

    Args:
        env: OpenAI Gym environment instance.
        Q (np.ndarray): Array of shape (s, a) containing the Q-table.
        lambtha (float): Eligibility trace decay factor.
        episodes (int): Total number of episodes to train over.
        max_steps (int): Maximum number of steps per episode.
        alpha (float): Learning rate.
        gamma (float): Discount factor.
        epsilon (float): Initial epsilon for the epsilon-greedy policy.
        min_epsilon (float): Minimum epsilon value.
        epsilon_decay (float): Decay rate for updating epsilon between episodes.

    Returns:
        np.ndarray: The updated Q-table.
    """
    n_actions = Q.shape[1]

    for episode in range(episodes):
        state = env.reset()
        # Initialize eligibility traces as a matrix of zeros
        E = np.zeros_like(Q)

        # Choose initial action using epsilon-greedy policy
        if np.random.random() < epsilon:
            action = np.random.randint(n_actions)
        else:
            action = np.argmax(Q[state])
        
        for _ in range(max_steps):
            next_state, reward, done, _ = env.step(action)

            # Choose the next action using epsilon-greedy policy (if not terminal)
            if not done:
                if np.random.random() < epsilon:
                    next_action = np.random.randint(n_actions)
                else:
                    next_action = np.argmax(Q[next_state])
            else:
                next_action = None

            # Compute the TD target and error
            if not done:
                td_target = reward + gamma * Q[next_state, next_action]
            else:
                td_target = reward
            td_error = td_target - Q[state, action]

            # Update the eligibility trace for the current state-action pair
            E[state, action] += 1

            # Update Q for all state-action pairs
            Q += alpha * td_error * E

            # Decay eligibility traces
            E *= gamma * lambtha

            # Prepare for next step
            state = next_state
            action = next_action if next_action is not None else None

            if done:
                break

        # Decay epsilon after each episode
        epsilon = max(min_epsilon, epsilon * (1 - epsilon_decay))

    return Q
