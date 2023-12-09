import numpy as np

class test_5:
    network_polarization = np.linspace(0, 1, num=13)
    opinion_polarization = 0
    treshold = 0.414
    path = "test/test_5/test_5_4_results/"
    number_of_iterations = 300
    echo_chamber_fraction = 0.20
    opinion_metric_steps = [0.01, 0.04, 0.08, 0.10, 0.12, 0.16, 0.20, 0.33, 0.66]
    nb_nodes = 100
    total_ticks = 100

class NetlogoCommands:

    def __init__(self, netlogo, modelfile):
        self.netlogo = netlogo
        self.modelfile = modelfile
    
    def get_a_active_agents(self):
        return self.netlogo.report("get-a-active-agents")
    
    def get_b_active_agents(self):
        return self.netlogo.report("get-b-active-agents")
    
    def get_neutral_agents(self):
        return self.netlogo.report("get-neutral-agents")
    
    def get_total_agents(self):
        return self.netlogo.report("get-total-agents")

    def get_global_cascade_fraction(self):

        active_a_agents = self.get_a_active_agents()
        total_agents = self.get_total_agents()
        return active_a_agents / total_agents
    
    def get_total_ticks(self):
        return self.netlogo.report("total-ticks")

    def set_total_ticks(self, value):
        return self.netlogo.command("set total-ticks {}".format(value))
    
    def set_opinion_polarization(self, value):
        self.netlogo.command("set P_O {}".format(value))

    def set_network_polarization(self, value):
        self.netlogo.command("set P_N {}".format(value))
    
    def set_treshold(self, value):
        self.netlogo.command("set teta {}".format(value))
    
    def set_nodes(self, value):
        self.netlogo.command("set nb-nodes {}".format(value))

    def set_initial_opinion_metric_value(self, value):
        self.netlogo.command("set initial-opinion-metric-value {}".format(value))
    
    def set_opinion_metric_step(self, value):
        self.netlogo.command("set opinion-metric-step {}".format(value))

    def set_echo_chamber_fraction(self, value):
        self.netlogo.command("set echo-chamber-fraction {}".format(value))

    def setup(self):
        self.netlogo.command('setup')
    
    def go(self):
        self.netlogo.command('go')

def calculate_fraction(values):
    count = 0
    for i in range(len(values)):
        if (values[i]> 0.5):
            count += 1
    
    return count/len(values)