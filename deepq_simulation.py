import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow import keras
import pynetlogo as pyNetLogo
import os
from collections import deque
import random
from environment.fake_news_diffusion_env import FakeNewsSimulation
from netlogo.simulation_controls import NetlogoCommands
import seaborn as sns
import matplotlib.pyplot as plt
import gymnasium as gym
import time


plt.rcParams["figure.figsize"] = (10, 5)
f, axis = plt.subplots(2, sharex=True)

netlogo = pyNetLogo.NetLogoLink(gui=False)
modelfile = os.path.abspath('./netlogo/FakeNewsSimulation.nlogo')
netlogoCommands = NetlogoCommands(netlogo, modelfile)
env = FakeNewsSimulation(netlogoCommands)

def agent(state_shape, action_shape):

    learning_rate = 0.001
    init = tf.keras.initializers.HeUniform()
    model = keras.Sequential()
    model.add(keras.layers.Dense(24, input_shape=state_shape, activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(12, activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(action_shape, activation='linear', kernel_initializer=init))
    model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), metrics=['accuracy'])
    return model

def get_qs(model, state, step):
    return model.predict(state.reshape([1, state.shape[0]]))[0]

def check_tuple(x):
    if isinstance(x, tuple):
        return x[0]
    else:
        return x

def train(env, replay_memory, model, target_model, done):
    learning_rate = 0.7 # Learning rate
    discount_factor = 0.618

    MIN_REPLAY_SIZE = 1000
    if len(replay_memory) < MIN_REPLAY_SIZE:
        return

    #batch_size = 64 * 2
    batch_size = 128
    mini_batch = random.sample(replay_memory, batch_size)

    array = [transition[0] for transition in mini_batch]
    current_states = tf.constant([check_tuple(array[0])])

    for i in range(1, len(array)):        
        y = tf.constant([check_tuple(array[i])])
        current_states = tf.concat([current_states,y], 0)

    current_qs_list = model.predict(current_states)
    new_current_states = np.array([transition[3] for transition in mini_batch])
    future_qs_list = target_model.predict(new_current_states)

    X = []
    Y = []
    for index, (observation, action, reward, new_observation, done) in enumerate(mini_batch):
        if not done:
            max_future_q = reward + discount_factor * np.max(future_qs_list[index])
        else:
            max_future_q = reward

        current_qs = current_qs_list[index]
        current_qs[action] = (1 - learning_rate) * current_qs[action] + learning_rate * max_future_q

        X.append(check_tuple(observation))
        Y.append(current_qs)
    model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)

    
def main():
    epsilon = 1 # Epsilon-greedy algorithm in initialized at 1 meaning every step is random at the start
    max_epsilon = 1 # You can't explore more than 100% of the time
    min_epsilon = 0.01 # At a minimum, we'll always explore 1% of the time
    decay = 0.01

    # 1. Initialize the Target and Main models
    # Main Model (updated every 4 steps)
    print(env.observation_space.shape, env.action_space)
    model = agent(env.observation_space.shape, env.action_space.n)
    # Target Model (updated every 100 steps)
    target_model = agent(env.observation_space.shape, env.action_space.n)
    target_model.set_weights(model.get_weights())

    replay_memory = deque(maxlen=50_000)

   
    print("Action Space: {}".format(env.action_space))
    print("State space: {}".format(env.observation_space))

    # X = states, y = actions
    X = []
    y = []

    target_update_counter = 0
    steps_to_update_target_model = 0
    reward_over_episodes = []
    wrapped_env = gym.wrappers.RecordEpisodeStatistics(env, 100)
    total_training_episodes = int(100)
    total_test_episodes = int(100)
    #rewards = []
    total_rewards = []

    start_time = time.time()

    env.set_most_influent_a_nodes_criteria(10, netlogoCommands.PAGERANK)

    for episode in range(total_training_episodes):
        total_training_rewards = 0
        observation = wrapped_env.reset()
        observation = check_tuple(observation)
        terminated = False
        while not terminated:

            steps_to_update_target_model += 1
            random_number = np.random.rand()
            if random_number <= epsilon:
                action = wrapped_env.action_space.sample()
            else:
                encoded = observation
                encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
                predicted = model.predict(encoded_reshaped).flatten()
                action = np.argmax(predicted)
            new_observation, reward, terminated, done, info = wrapped_env.step(action)
            #rewards.append(reward)
            replay_memory.append([observation, action, reward, new_observation, terminated])
            
            if steps_to_update_target_model % 4 == 0 or terminated:
                train(env, replay_memory, model, target_model, terminated)

            observation = new_observation
            total_training_rewards += reward

            if terminated:
                print('Total training rewards: {} after n steps = {} with final reward = {}'.format(total_training_rewards, episode, reward))

                if steps_to_update_target_model >= 100:
                    print('Copying main network weights to the target network weights')
                    target_model.set_weights(model.get_weights())
                    steps_to_update_target_model = 0
                break

                
        reward_over_episodes.append(wrapped_env.return_queue[-1])
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

    total_rewards.append(reward_over_episodes)

    total_training_time = (time.time() - start_time)/60


    rewards_to_plot = [[reward[0] for reward in rewards] for rewards in total_rewards]
    df1 = pd.DataFrame(rewards_to_plot).melt()
    df1.rename(columns={"variable": "episodes", "value": "reward"}, inplace=True)
    sns.set(style="darkgrid", context="talk", palette="rainbow")
    sns.lineplot(x="episodes", y="reward", data=df1, ax= axis[0], label="training rewards").set(
        title="DeepQLearning Train for FakeNewsDetection"
    )
    #plt.show()


    total_rewards = []
    reward_over_episodes = []
    global_cascade = []
    start_time = time.time()

    #Testing the model generated from training episodes
    for episode in range(total_test_episodes):
        total_test_rewards = 0
        observation = wrapped_env.reset()
        observation = check_tuple(observation)
        terminated = False
        
        while not terminated:

            encoded = observation
            encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
            predicted = target_model.predict(encoded_reshaped).flatten()
            action = np.argmax(predicted)
            new_observation, reward, terminated, done, info = wrapped_env.step(action)
            #rewards.append(reward)
            replay_memory.append([observation, action, reward, new_observation, terminated])
            
            observation = new_observation
            total_test_rewards += reward

            if terminated:
                print('Total test rewards: {} after n steps = {} with final reward = {}'.format(total_test_rewards, episode, reward))
                global_cascade.append(observation[0])

                
        reward_over_episodes.append(wrapped_env.return_queue[-1])

    total_rewards.append(reward_over_episodes)

    total_testing_time = (time.time() - start_time)/60
    print("Training time %s minutes ---" % total_training_time)
    print("Testing time %s minutes ---" % total_testing_time)
    print("Totaltime {} minutes ---".format(total_training_time+total_testing_time))


    rewards_to_plot = [[reward[0] for reward in rewards] for rewards in total_rewards]
    df1 = pd.DataFrame(rewards_to_plot).melt()
    df1.rename(columns={"variable": "episodes", "value": "reward"}, inplace=True)
    sns.set(style="darkgrid", context="talk", palette="rainbow")
    sns.lineplot(x="episodes", y="reward", data=df1, ax=axis[0], label="test rewards").set(
        title="DeepQLearning Test for FakeNewsDetection"
    )
    df2 = pd.DataFrame({"episodes": [i for i in range(total_test_episodes)], "global cascade": global_cascade})
    sns.lineplot(ax = axis[1], x = "episodes", y = "global cascade", data = df2, label="global cascade").set(
        title="Global cascade during test"
    )
    legend = plt.legend()
    plt.show()

    env.close()
    netlogo.kill_workspace()

if __name__ == '__main__':
    main()