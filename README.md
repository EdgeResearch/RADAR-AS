# "RADAR-AS: Reinforcement-Aided Detection and Active Response with Agent-Based Simulation against Disinformation"

## The Simulation Model

The full description of the model that simulates the spread of fake news within a network is presented here. 
The description follows the **ODD** protocol. The model was implemented on NetLogo 6.2.0.

### Goals 🎯
The simulation model was developed to study the spread of fake news on social networks and examine its potential correlation with the echo chamber phenomenon on these platforms. Built with simplicity and generalizability in mind, the model aims to produce straightforward and interpretable results. To support this, a web platform was created, enabling users to customize and launch simulations with clear, comprehensive, and interactive result visualizations. Additionally, the model is designed to be highly adaptable, allowing for the simulation of various social networks and the spread of different types of information.
### The simulation agents 👥
The simulation model includes two types of agents: **basic-agents** and a **super-agent**.

**Basic Agents**

Basic-agents are the nodes that make up the social network—representing users of the platform. Each node is assigned an *activation threshold*, which determines how easily the user can be convinced by a particular narrative or news item. If a sufficient number of a node's adjacent nodes (*neighboring users*) promote a given narrative and exceed its threshold, that node will be **activated** and will begin to spread the narrative as well.

In the simulation, agents can adopt one of three opinion types:

- **Opinion A**, which supports the *false news* (represented by *orange-colored nodes*).
- **Opinion B**, which supports *factual information* (represented by *blue-colored nodes*).
- **Neutral opinion**, indicating *indecision or lack of knowledge* on the topic (represented by *gray-colored nodes*).

To make the simulation more realistic, agents within the network do not change their opinion merely by exceeding a threshold. Instead, they have a "credibility margin," represented by the "**opinion metric**" attribute. This parameter is a decimal value that determines the agent's opinion in the network according to specific rules.
- If the value is between 0 and 0.33, the agent holds an opinion of type B.
- If the value is between 0.34 and 0.65, the agent has no opinion, so it is neutral.
- If the value is between 0.66 and 1, the agent holds an opinion of type A.

There is an additional parameter, "**opinion metric step**", which determines how much the opinion metric should change when the agent receives an opinion of type A or B. This parameter controls the speed at which the basic agents change their opinion: higher values result in faster changes.

**Super Agent**

The **super-agent** is a higher-level entity in the simulation, capable of *constantly monitoring* the network's state and the spread of information. Based on its observations, it can determine which actions to take to *mitigate the effects of misinformation*. Implemented using a reinforcement learning algorithm called **Deep Double Q-Network (DDQN)**, the super-agent is designed to observe the network's status and select the most effective actions to reduce the spread of fake news. This entity can be viewed as a *social network administrator* or as a *manual or automated counter-disinformation system* responsible for managing and monitoring information within the network.  This entity interacts with the environment and, at each time step, selects the *most appropriate action* to maximize a **reward value**. This reward reflects the *effectiveness* of its actions in reducing the *virality of misinformation*.

### The contrast actions of the super-agent 🛑
The super-agent, in order to limit and counter the proliferation of fake news within the network, can undertake the following actions:

**Warning** \
An effective strategy to limit the spread of misinformation on social networks is prevention. One approach involves showing users a warning that alerts them when a news item lacks verified sources or originates from an unreliable source, suggesting it may be fake.  In our simulation, the super-agent can emulate this behavior through a "Warning" action. This action sends an alert to one or more basic agents in the simulation, setting their warning variable to true, which remains active until the simulation ends. If the warning is "global," it reaches all agents; otherwise, agents are chosen based on relevant properties. To model user response to a warning, two additional parameters, "warning-impact" and "warning-impact-neutral" (both ranging from 0 to 1), adjust the warning's influence based on whether agents hold an "A" opinion or a neutral stance. When a basic agent is activated and influenced by an opinion, it checks whether its warning variable is true. If so, a random number between 0 and 1 is generated and compared to the corresponding warning-impact value. If the number is lower than warning-impact, the basic agent shifts to opinion B, simulating a user who heeds the warning. Thus, the higher the warning-impact value, the more effectively this counteraction limits the spread of fake news.

**Reiterate** \
In social networks, especially within echo chambers, the "continued influence effect" often occurs. This effect describes the tendency of people to rely on false information even after it has been corrected or debunked. Social and psychological factors, like mental model building and retrieval difficulties, lead people to remember the misinformation rather than the correction.  In the simulation, the super-agent can counteract this effect through a "Reiterate" function, which repeatedly shows users the accurate information to encourage opinion change. However, the super-agent must avoid repeating the misinformation too often, as increased familiarity with false content can inadvertently strengthen its influence. Technically, a set of basic agents is selected to apply this action, setting the variable `reiterate == true`. When one of these agents is about to change its opinion, it will be exposed to a number of type B (truthful) news items equal to the number of its adjacent nodes.

**Static B Agents** \
The last action the super-agent can perform is ensuring that certain entities within the network remain reliable, such as trusted news outlets or reputable organizations that consistently publish truthful news, regardless of the prevailing opinion on the network.  The super-agent can select a set of nodes to maintain opinion B throughout the simulation. These nodes can be chosen based on metrics like betweenness, page rank, degree, or randomly. The number of agents is determined by the parameter `node-range-static-b` (a real value between 0 and 1). Technically, the opinion metric for these nodes is set to 0, and the `is-opinion-b-static` variable prevents the node from changing its opinion.





## Process Overview and Planning ⚙️

At the beginning of the simulation, the number of nodes that make up the network, the number of *ticks* determining the duration of the simulation, and the type of network to be created are selected. The network can be one of the following types: *Erdős–Rényi*, *Small World*, or *Preferential Attachment*. Based on the selected network type, the parameters for creating the connections between nodes are set. For an *Erdős–Rényi* network, a parameter *k* is set, determining the value of the normal distribution used to generate the number of connections each node should have, along with the standard deviation. In the case of a *Small World* network, the *Neighborhood Size* and *Rewire Probability* are selected. These correspond to the number of nodes to which each node should be connected, and the probability that each edge will be disconnected from one of its ends and reconnected to another randomly chosen node in the network. Finally, for the *Preferential Attachment* network, a "scale-free" network is generated, where agents are added one by one, each forming a minimum number of links (one in our case) with previously added nodes. The more connections a node has, the greater the chance that new nodes will connect to it when added.

### Echo Chamber 📢

Once the network is created, the echo chamber is initialized, consisting of nodes that support the opinion of the fake news. The echo chamber is characterized by two properties: *opinion polarization* and *network polarization*. 

- *Opinion polarization* means that users, in relation to an opinion, are more likely to share similar views.
- *Network polarization* means that users are more connected to each other than to the rest of the network.

In other words, an echo chamber has tightly connected nodes that tend to share the same opinion on a particular narrative. The values of *Po* and *Pn* are set, and the fraction of nodes that should belong to the echo chamber is chosen through the *echo chamber fraction* parameter. At the beginning of the creation process, this fraction is multiplied by the number of nodes to determine how many nodes should be placed in the echo chamber. 

The calculation to obtain the number of edges is: 'E = N * Pn' where *E* is the number of edges, *N* is the number of nodes, and *Pn* is the network polarization factor. The value of *E* determines how many edges should be chosen from the total set of edges in the network. A random check is then performed on all the selected edges to see if exactly one of the nodes at either end belongs to the echo chamber. If so, the edge is removed and replaced with a connection between a node that already belongs to the echo chamber and another that does as well. This increases the degree of connectivity between nodes in the echo chamber, creating more cohesion. 

Next, a random node from the echo chamber is selected to serve as the activation point, where its opinion is set to type A (and a random value of the *opinion metric* is assigned within the range corresponding to opinion A). This node and all its connected nodes are also activated. The same procedure is repeated for nodes of type B, where a node outside the echo chamber is chosen, set to type B, and all connected nodes that don't already have type A or belong to the echo chamber are activated.

Once this process is complete, the activation threshold *Θ* is set for each node in the network. Specifically, for nodes within the echo chamber, *Θ* is adjusted to *Θ - Po*, while for other nodes, the value of *Θ* is simply the one chosen at the start of the simulation.

### Super Agent 🤖

After the network and echo chamber are set up, the super agent is inserted into the network. This type of agent has no attributes and has three actions available to counteract the spread of opinion A during the simulation and reduce the *global cascade*, which corresponds to the fraction of active nodes with opinion A. The actions are: *warning*, *reiterate*, and *static B nodes*. 

During the placement of the super agent, it is connected to a number of nodes specified by the *node-range* parameter. The nodes are selected based on their *betweenness*, *page rank*, or *degree*, and calculations are performed at each simulation step to create the connections, as these values may change over time. Additionally, if the super agent already has connections, they are removed and replaced with new ones.

### Simulation Process 📊

Once the network is initialized, the simulation can begin. The model proceeds in time steps determined by the *ticks*. At the beginning of each step, it is checked if any of the three actions have been activated, ensuring that only one action is triggered per tick. If an agent changes its opinion during a tick, the opinion is considered active towards type A or B only in the next step.

Next, all *basic agents* are asked to count the number of neighboring nodes of type A or B and calculate their respective fractions. Based on the dominant fraction, it is compared to the activation threshold. If the fraction exceeds the threshold *Θ*, the *opinion metric* is calculated. If the fractions of type A and B are equal, a random choice is made regarding which opinion will influence the agent.

After the main news diffusion procedure, the actions of the super agent (if active) are applied. At the end of the simulation, once the specified number of *ticks* has been reached, the *global cascade* is calculated.

## The Simulation Platform 🖥️
### Goals 🎯
The platform has been designed to optimize the management of simulations, making it simple and efficient. A key component is the user-friendly graphical interface, which ensures intuitive interaction, even for users with limited technical expertise. By being hosted on a web platform, it remains accessible anytime and from any internet-connected device, offering high operational flexibility.

Another goal of the platform is to provide a clear and detailed description of all simulation components, including parameters, options, and functionalities. The interface allows users to easily access detailed explanations for each element, fostering a better understanding and conscious use of the system.

A crucial aspect of the platform is its ability to present simulation results immediately and in a ready-to-use format, eliminating the need for manual data processing and enabling quick interpretation of the outputs. After each simulation, results are displayed in interactive graphs and can be easily downloaded for further analysis or storage.

Finally, to enhance understanding and control of the simulation process, the system offers real-time visualization of logs generated during execution. These logs are accessible during the simulation and can be reviewed and downloaded afterward, providing users with an additional tool for monitoring and analysis.

### Tech Stack 💾
**Back-end:** Python, “bottle” library for server implementation

**Front-end:** HTML, CSS, JavaScript

### System Architecture 🏗️

The simulation platform is built on a Client/Server architecture, where the subsystem called *Server* provides specific services (in this case, running simulations), while the Clients are the users accessing these services. This architecture is particularly well-suited for implementing the system, as it allows the simulation model to be centralized, eliminating the need for users to manage technical or implementation aspects.

In the context of the developed platform, interaction occurs via HTTP messages. The server is available on the internet and is primarily responsible for managing all simulation processes from start to finish. Meanwhile, the Client represents the user interface, accessible through a simple web browser by connecting to the server via its unique URL.

Thanks to this configuration, the design and development perfectly align with the initial objectives. Users can interact with the platform from anywhere, using an internet connection, without needing to install additional software. Moreover, this solution offers efficient resource management, making it easier to update and maintain the system on the server side, while users enjoy easy and immediate access through the Client, providing an intuitive and direct interface with the platform's features.
