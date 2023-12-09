import numpy as np
import tensorflow as tf
from tensorflow import keras
from collections import deque
import random
import gymnasium as gym
import time


class DeepQLearning:
    
    def agent(self, state_shape, action_shape):

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

    def check_tuple(self, x):
        if isinstance(x, tuple):
            return x[0]
        else:
            return x

    def train(self, env, replay_memory, model, target_model, done):
        learning_rate = 0.7 # Learning rate
        discount_factor = 0.618

        MIN_REPLAY_SIZE = 1000
        if len(replay_memory) < MIN_REPLAY_SIZE:
            return

        #batch_size = 64 * 2
        batch_size = 128
        mini_batch = random.sample(replay_memory, batch_size)

        array = [transition[0] for transition in mini_batch]
        current_states = tf.constant([self.check_tuple(array[0])])

        for i in range(1, len(array)):        
            y = tf.constant([self.check_tuple(array[i])])
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

            X.append(self.check_tuple(observation))
            Y.append(current_qs)
        model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)

        
    def run_model_training(self, env, netlogoCommands, iterations):
        epsilon = 1 # Epsilon-greedy algorithm in initialized at 1 meaning every step is random at the start
        max_epsilon = 1 # You can't explore more than 100% of the time
        min_epsilon = 0.01 # At a minimum, we'll always explore 1% of the time
        decay = 0.01

        # 1. Initialize the Target and Main models
        # Main Model (updated every 4 steps)
        #netlogoCommands = netlogoCommands
        #self.env = env
        #print(env.observation_space.shape, env.action_space)
        print("Resetting model and target model")
        self.model = self.agent(env.observation_space.shape, env.action_space.n)
        self.target_model = self.agent(env.observation_space.shape, env.action_space.n)
        self.target_model.set_weights(self.model.get_weights())

        replay_memory = deque(maxlen=10_000)

        print("Action Space: {}".format(env.action_space))
        print("State space: {}".format(env.observation_space))

        X = []
        y = []

        target_update_counter = 0
        steps_to_update_target_model = 0
        reward_over_episodes = []
        wrapped_env = gym.wrappers.RecordEpisodeStatistics(env, 100)
        total_training_episodes = iterations
        total_test_episodes = iterations
        total_rewards = []

        start_time = time.time()

        for episode in range(total_training_episodes):
            total_training_rewards = 0
            observation = wrapped_env.reset()
            observation = self.check_tuple(observation)
            terminated = False
            while not terminated:

                steps_to_update_target_model += 1
                random_number = np.random.rand()
                if random_number <= epsilon:
                    action = wrapped_env.action_space.sample()
                else:
                    encoded = observation
                    encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
                    predicted = self.model.predict(encoded_reshaped).flatten()
                    action = np.argmax(predicted)
                new_observation, reward, terminated, done, info = wrapped_env.step(action)
                replay_memory.append([observation, action, reward, new_observation, terminated])
                
                if steps_to_update_target_model % 4 == 0 or terminated:
                    self.train(env, replay_memory, self.model, self.target_model, terminated)

                observation = new_observation
                total_training_rewards += reward

                if terminated:
                    print('Total training rewards: {} after n steps = {} with final reward = {}'.format(total_training_rewards, episode, reward))

                    if steps_to_update_target_model >= 100:
                        print('Copying main network weights to the target network weights')
                        self.target_model.set_weights(self.model.get_weights())
                        steps_to_update_target_model = 0
                    break

                    
            reward_over_episodes.append(wrapped_env.return_queue[-1])
            epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

        total_rewards.append(reward_over_episodes)

        total_training_time = (time.time() - start_time)/60
        print("Training time %s minutes ---" % total_training_time)
    
    def predict_sa_action(self, env, observation):
        observation = self.check_tuple(observation)
        encoded = observation
        encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
        predicted = self.target_model.predict(encoded_reshaped).flatten()
        action = np.argmax(predicted)
        new_observation, reward, terminated, done, info = env.step(action)
        return new_observation, reward, terminated, done, info, action


