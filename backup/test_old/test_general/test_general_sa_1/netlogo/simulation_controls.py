class NetlogoCommands:

    BETWENNESS = "betweenness"
    PAGERANK = "page-rank"
    DEGREE = "degree"

    def __init__(self, netlogo, modelfile):
        self.netlogo = netlogo
        self.modelfile = modelfile
        self.netlogo.load_model(modelfile)
        
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

    def get_current_tick(self):
        return self.netlogo.report("get-current-tick")
    
    def get_total_ticks(self):
        return self.netlogo.report("get-total-ticks")

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

    
