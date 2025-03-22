    #!/usr/bin/env python3
import numpy as np

def monte_carlo(env, V, policy, episodes=5000, max_steps=100, alpha=0.1, gamma=0.99):
    """
    Performs the Monte Carlo algorithm to update the state-value function V.

    Args:
        env: OpenAI Gym environment instance.
        V (np.ndarray): Array of shape (s,) containing the value estimates.
        policy (function): A function that takes a state and returns an action.
        episodes (int): Total number of episodes to train over.
        max_steps (int): Maximum number of steps per episode.
        alpha (float): Learning rate.
        gamma (float): Discount factor.

    Returns:
        np.ndarray: The updated value estimate V.
    """
    for _ in range(episodes):
        state = env.reset()
        episode = []
        # Generate an episode
        for _ in range(max_steps):
            action = policy(state)
            next_state, reward, done, _ = env.step(action)
            episode.append((state, reward))
            state = next_state
            if done:
                break

        G = 0
        # Traverse the episode backwards to compute returns and update V
        for state, reward in reversed(episode):
            G = gamma * G + reward
            V[state] += alpha * (G - V[state])
    return V
