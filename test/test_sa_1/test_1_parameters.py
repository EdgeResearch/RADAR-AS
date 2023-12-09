import numpy as np

class test_sa_1:
    network_polarization = np.linspace(0, 1, num=13)
    opinion_polarization = 0
    tresholds = [0.270, 0.342, 0.414]
    number_of_iterations = 100
    echo_chamber_fraction = 0.20
    opinion_metric_step = 0.10
    nb_nodes = 100
    path = "test/test_sa_1/test_sa_1_results/"
    warning = "global"
    node_range_static_b = 0.05
    node_range = 0.10
    choose_method = "degree"
    warning_impact = 0.10
    warning_impact_neutral = 0.30
    sa_delay = 5


class NetlogoCommands:

    BETWENNESS = "betweenness"
    PAGERANK = "page-rank"
    DEGREE = "degree"

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
    
    def get_most_influent_a_nodes(self, node_span, criteria):
        match criteria:
            case self.DEGREE:
                return self.netlogo.report('get-most-influent-a-nodes-by-degree {}'.format(node_span))
            case self.PAGERANK:
                return self.netlogo.report('get-most-influent-a-nodes-by-page-rank {}'.format(node_span))
            case self.BETWENNESS:
                return self.netlogo.report('get-most-influent-a-nodes-by-betweenness {}'.format(node_span))
    
    def get_global_opinion_metric_mean(self):
        return self.netlogo.report('get-global-opinion-metric-mean')
    
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

    def set_warning(self, value):
        if (value == "global"):
            self.netlogo.command("set global-warning true")
        else:
            self.netlogo.command("set global-warning false")
    
    def set_node_range(self, value):
        self.netlogo.command("set node-range {}".format(value))
    
    def set_node_range_static_b(self, value):
        self.netlogo.command("set node-range-static-b {}".format(value))

    def set_warning_impact(self, value):
        self.netlogo.command("set warning-impact {}".format(value))
    
    def set_warning_impact_neutral(self, value):
        self.netlogo.command("set warning-impact-neutral {}".format(value))
    
    def set_echo_chamber_fraction(self, value):
        self.netlogo.command("set echo-chamber-fraction {}".format(value))
    
    def get_current_tick(self):
        return self.netlogo.report("get-current-tick")
    
    def get_total_ticks(self):
        return self.netlogo.report("total-ticks")

    def setup(self):
        self.netlogo.command('setup')
    
    def go(self):
        self.netlogo.command('go')
    
    def activate_warning(self):
        self.netlogo.command('activate-warning')
    
    def activate_reiterate(self):
        self.netlogo.command('activate-reiterate')

    def activate_static_b_node(self):
        self.netlogo.command('activate-static-b-agents')

    def choose_action(self, choice):
        match choice:
            case 0:
                self.go()
            case 1:
                self.activate_warning()
                self.go()
            case 2:
                self.activate_reiterate()
                self.go()
            case 3:
                self.activate_static_b_node()
                self.go()

def calculate_fraction(values):
    count = 0
    for i in range(len(values)):
        if (values[i]> 0.5):
            count += 1
    
    return count/len(values)