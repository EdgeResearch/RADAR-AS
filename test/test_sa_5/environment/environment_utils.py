from netlogo.simulation_parameters import NetlogoSimulationParameters

class EnvironmentUtils():

    global_cascade_values = []
    reward_cascade_decrease = 2
    maximum_reward_value = 10

    def CalculateReward2(self, action, tick, global_cascade):
        reward = 0
        if (global_cascade < 0.5):
            reward = 1
        return reward
        

    def CalculateReward1(self, action, tick, global_cascade, most_influent_a_nodes, opinion_metric_mean, warning, static_b):
        reward = 0
        action_weight = (1 - most_influent_a_nodes) + (1 - opinion_metric_mean) 

        if (tick != 1):
            latest_global_cascade = self.global_cascade_values[tick-1]
            action_result = global_cascade - latest_global_cascade

            #warning
            if (action == 1):
                if (warning == False):
                    if (action_result <= 0):
                        reward = (1 + action_weight) * 0.5
                        reward -= action_result
                    else:
                        reward = (0 + action_weight) * 0.5
                else:
                    #Se il warning è stato già eseguito almeno una volta, allora vale quanto un'azione "go"
                    if (global_cascade > 0.5):
                        reward = 0
                    else:
                        reward = 1
            #reiterate
            elif (action == 2):
                if (action_result <= 0):
                    reward = (1 + action_weight) * 0.5
                    reward -= action_result
                else:
                    reward = (0 + action_weight) * 0.5
            #static b
            elif (action == 3):
                if (static_b == False):
                    if (action_result <= 0):
                        reward = (1 + action_weight) * 0.5
                        reward -= action_result
                    else:
                        reward = (0 + action_weight) * 0.5
                else:
                    #Se static b è stato già eseguito almeno una volta, allora vale quanto un'azione "go"
                    if (global_cascade > 0.5):
                        reward = 0
                    else:
                        reward = 1
            #go
            else:
                if (action_result <= 0):
                    reward = 1
                else:
                    reward = 0
        return reward

    def CalculateReward(self, action, tick, global_cascade):
        reward = 1
        if (tick != 1):
            latest_global_cascade = self.global_cascade_values[tick-1]
            action_result = global_cascade - latest_global_cascade
            match(action):
                case 0:
                    if (global_cascade == 0):
                        reward = self.maximum_reward_value / NetlogoSimulationParameters.GoWeight + self.reward_cascade_decrease
                    elif (global_cascade > 0.5):
                        if (action_result < 0):
                            reward = - action_result * NetlogoSimulationParameters.GoWeight
                        elif (action_result == 0):
                            reward = 0.5
                        elif (action_result > 0):
                            reward = action_result / NetlogoSimulationParameters.GoWeight
                    elif (global_cascade <= 0.5):
                        if (action_result < 0):
                            reward = (- action_result * NetlogoSimulationParameters.GoWeight) + self.reward_cascade_decrease
                        elif (action_result == 0):
                            reward = 1
                        elif (action_result > 0):
                            reward = (action_result / NetlogoSimulationParameters.GoWeight) + self.reward_cascade_decrease - 1
                case 1:
                    if (global_cascade == 0):
                        reward = self.maximum_reward_value / NetlogoSimulationParameters.WarningWeight + self.reward_cascade_decrease
                    elif (global_cascade > 0.5):
                        if (action_result < 0):
                            reward = - action_result * NetlogoSimulationParameters.WarningWeight
                        elif (action_result == 0):
                            reward = 0.5
                        elif (action_result > 0):
                            reward = action_result / NetlogoSimulationParameters.WarningWeight
                    elif (global_cascade <= 0.5):
                        if (action_result < 0):
                            reward = (- action_result * NetlogoSimulationParameters.WarningWeight) + self.reward_cascade_decrease
                        elif (action_result == 0):
                            reward = 1
                        elif (action_result > 0):
                            reward = (action_result / NetlogoSimulationParameters.WarningWeight) + self.reward_cascade_decrease - 1
                case 2:
                    if (global_cascade == 0):
                        reward = self.maximum_reward_value / NetlogoSimulationParameters.ReiterateWeight + self.reward_cascade_decrease
                    elif (global_cascade > 0.5):
                        if (action_result < 0):
                            reward = - action_result * NetlogoSimulationParameters.ReiterateWeight
                        elif (action_result == 0):
                            reward = 0.5
                        elif (action_result > 0):
                            reward = action_result / NetlogoSimulationParameters.ReiterateWeight
                    elif (global_cascade <= 0.5):
                        if (action_result < 0):
                            reward = (- action_result * NetlogoSimulationParameters.ReiterateWeight) + self.reward_cascade_decrease
                        elif (action_result == 0):
                            reward = 1
                        elif (action_result > 0):
                            reward = (action_result / NetlogoSimulationParameters.ReiterateWeight) + self.reward_cascade_decrease - 1
                case 3:
                    if (global_cascade == 0):
                        reward = self.maximum_reward_value / NetlogoSimulationParameters.StaticWeight + self.reward_cascade_decrease
                    elif (global_cascade > 0.5):
                        if (action_result < 0):
                            reward = - action_result * NetlogoSimulationParameters.StaticWeight
                        elif (action_result == 0):
                            reward = 0.5
                        elif (action_result > 0):
                            reward = action_result / NetlogoSimulationParameters.StaticWeight
                    elif (global_cascade <= 0.5):
                        if (action_result < 0):
                            reward = (- action_result * NetlogoSimulationParameters.StaticWeight) + self.reward_cascade_decrease
                        elif (action_result == 0):
                            reward = 1
                        elif (action_result > 0):
                            reward = (action_result / NetlogoSimulationParameters.StaticWeight) + self.reward_cascade_decrease - 1
        
        return reward

    def AddValue(self, global_cascade):
        self.global_cascade_values.append(global_cascade)

    def ResetList(self):
        self.global_cascade_values = []