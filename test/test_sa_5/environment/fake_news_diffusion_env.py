from gymnasium import Env, spaces
import numpy as np
from environment.environment_utils import EnvironmentUtils
from netlogo.simulation_controls import NetlogoCommands
from netlogo.simulation_parameters import NetlogoSimulationParameters

class FakeNewsSimulation(Env):
    netlogo = 0
    environment_utils = 0
    def __init__(self, netlogoCommands : NetlogoCommands):
        super(FakeNewsSimulation, self).__init__()

        print("Initialinzing the environment...")
        
        self.netlogo = netlogoCommands
        self.environment_utils = EnvironmentUtils()

        low = np.array([0.0, 0.0, 0.0])
        high = np.array([1.0, 1.0, 1.0])
        self.observation_space = spaces.Box(low, high, dtype=np.float32)
        self.action_space = spaces.Discrete(4)

        self.global_cascade = 0
        self.most_influent_b_nodes = 0
        self.global_opinion_metric_mean = 0
        self.node_span = 0
        self.criteria = ""
        self.warning = False
        self.static_b = False
        self.elements = []
    
    def set_most_influent_a_nodes_criteria(self, node_span, criteria):
        self.node_span = node_span
        self.criteria = criteria

    def reset(self, seed = None, options = None):

        super().reset(seed=seed)

        self.netlogo.setup() 
        self.global_cascade = self.netlogo.get_global_cascade_fraction()
        self.most_influent_b_nodes = self.netlogo.get_most_influent_a_nodes(self.node_span, self.criteria)
        self.global_opinion_metric_mean = self.netlogo.get_global_opinion_metric_mean()
        self.environment_utils.ResetList()
        self.environment_utils.AddValue(self.global_cascade)
        self.warning = False
        self.static_b = False
        return self.get_obs(), {}

    def get_info(self):
        return {
        }
    
    def get_obs(self):
        value = (self.global_cascade, self.most_influent_b_nodes, self.global_opinion_metric_mean)
        return np.array(value,dtype=np.float32)
    
    def step(self, action):

        terminated = False

        assert self.action_space.contains(action), "Invalid Action"

        reward = 1
        
        current_tick = self.netlogo.get_current_tick()

        self.netlogo.choose_action(action)

        if (current_tick >= NetlogoSimulationParameters.NumberOfTicks):
            terminated = True
         
        self.global_cascade = self.netlogo.get_global_cascade_fraction()
        self.most_influent_b_nodes = self.netlogo.get_most_influent_a_nodes(self.node_span, self.criteria)
        self.global_opinion_metric_mean = self.netlogo.get_global_opinion_metric_mean()

        self.environment_utils.AddValue(self.global_cascade)
        reward = self.environment_utils.CalculateReward1(action, int(self.netlogo.get_current_tick()), self.global_cascade, self.most_influent_b_nodes,
                                                          self.global_opinion_metric_mean, self.warning, self.static_b)

        if (action == 1):
            self.warning = True
        
        if (action == 3):
            self.static_b = True

        return self.get_obs(), reward, terminated, False, self.get_info()
    
    def close(self):
        self.netlogo.kill_workspace()