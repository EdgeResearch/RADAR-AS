extensions [nw]

directed-link-breed [directed-edges directed-edge]
undirected-link-breed [undirected-edges undirected-edge]
breed [super-agents super-agent]
breed [basic-agents basic-agent]

globals [
  neutral-agents             ;; Number of agents that does not suppor neither opinion a or b
  active-a-agents            ;; Number of agents that support the fake news (orange)
  active-b-agents            ;; Number of agents that does not support the fake news (blue)
  in-cluster-agents          ;; Number of agents that are initially positioned in the echo chamber
  total-number-agents        ;; Total number of nodes
  total-links                ;; Total number of edges
  k                          ;; Average degree of the network
  global-cascade             ;; This variable is true when the fraction of active-a nodes is greater of 50%, false otherwise
  is-warning-active          ;; Variable used by the super agent to initialize a warning
  is-reiterate-active        ;; Variable used by the super agent to initialize a reiterate
]

basic-agents-own [
  activation-treshold        ;; Determines how an agent is susceptible to change opinion
  betweenness                ;; Network analysis parameter
  eigenvector                ;;
  closeness                  ;;
  clustering                 ;;
  community                  ;;
  page-rank                  ;;
  in-degree                  ;;
  out-degree                 ;;
  degree                     ;;
  is-a-active                ;; True if the agent support the fake news
  is-b-active                ;; True if the agent does not support the fake news
  is-in-cluster              ;; True if the agent is located in the echo chamber
  is-active-next             ;; Ausiliary variable used to delay the change of opinion of an agent during the simulation. If true the agent will support the opinion a
  is-inactive-next           ;; Ausiliary variable used to delay the change of opinion of an agent during the simulation. If true the agent will support the opinion b
  warning                    ;; When this variable is set to true, the agent is warned that the opinion a is a fake news
  received-a-news-counter    ;; Counter of opinion a news received
  received-b-news-counter    ;; Counter of opinion b news received
  reiterate                  ;; When this variable is set to true, the agent will receive more opinion b news so that is more likely that he will change his opinion from a to b
  reiterate-counter          ;; Counter needed to determine whether or not the agent will reiterate his opinion
  opinion-metric             ;; Variable used to know when an agent is about to change opinion. The values are included between 0.00 and 1.00
  is-opinion-b-static        ;; Boolean that when set to true an agent will always sustain opinion b
]

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Setup
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

to setup
  clear-all
  set-default-shape turtles "circle"
  reset-ticks
  setup-patches
  setup-turtles
  if layout? [layout]
end

to setup-patches
  ask patches [ set pcolor black ]
end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Report
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;; Function used to determine whether to use directed or undirected edges
to-report get-links-to-use
  report ifelse-value (links-to-use = "directed")
    [ directed-edges ]
    [ undirected-edges ]
end

;; Function used to get the global cascade value
to-report get-cascade
  report global-cascade
end

;; Function used in the layout procedure to don't bump the edges of the world
to-report limit-magnitude [number limit]
  if number > limit [ report limit ]
  if number < (- limit) [ report (- limit) ]
  report number
end


;; Function used to get the count of total agents that are within the cluster(echo chamber)
to-report get-in-cluster-agents
  report count basic-agents with [is-in-cluster = true]
end

;; Function used to get the count of total active agents with opinion a
to-report get-a-active-agents
  report count basic-agents with [is-a-active = true]
end


;; Function used to get the count of total active agents with opinion b
to-report get-b-active-agents
  report count basic-agents with [is-b-active = true]
end

;; Function used to get the count of total neutral agents
to-report get-neutral-agents
  report count basic-agents with [is-a-active = false and is-b-active = false]
end

;; Function used to get the total number of basic agents
to-report get-total-agents
  report count basic-agents
end

;; Function used to get the current tick in the simulation
to-report get-current-tick
  report ticks
end

;; Function used to get the mean of the global opinion metric value
to-report get-global-opinion-metric-mean
  let x 0

  ask basic-agents[
    set x x + opinion-metric
  ]

  report x / get-total-agents
end

;; Function used to get the fraction of the top nodes by degree that have opinion a
to-report get-most-influent-a-nodes-by-degree [node-span]
  let agent-list sort-on[(- degree)] basic-agents
  let result sublist agent-list 0 min list node-span (length agent-list)
  let x 0
  let elements turtle-set result
  ask elements [
    if is-a-active = true [
      set x x + 1
    ]
  ]
  report x / 10
end

to-report get-most-influent-a-nodes-by-page-rank [node-span]
  let agent-list sort-on[(- page-rank)] basic-agents
  let result sublist agent-list 0 min list node-span (length agent-list)
  let x 0
  let elements turtle-set result
  ask elements [
    if is-a-active = true [
      set x x + 1
    ]
  ]
  report x / 10
end

to-report get-most-influent-a-nodes-by-betweenness [node-span]
  let agent-list sort-on[(- betweenness)] basic-agents
  let result sublist agent-list 0 min list node-span (length agent-list)
  let x 0
  let elements turtle-set result
  ask elements [
    if is-a-active = true [
      set x x + 1
    ]
  ]
  report x / 10
end


;; Function used to get the fraction of the top nodes by degree that have opinion A and are in the cluster
to-report get-most-influent-a-nodes-by-degree-in-cluster [node-span]
		let agent-list sort-on [(- degree)] basic-agents
		let result sublist agent-list 0 min list node-span (length agent-list)
		let x 0
		let elements turtle-set result
		;; Conta i nodi che sono attivi e che fanno parte del cluster
		ask elements [
			if (is-a-active = true) and (is-in-cluster = true) [
				set x x + 1
			]
		]
		report x / 10
end

to-report get-random-influent-a-nodes [node-span]
  ;; Seleziona node-span nodi casuali dalla lista di nodi
  let agent-list n-of node-span basic-agents
  let x 0
  let elements turtle-set agent-list
  let to_take node-span / 10
  let out_c 0
  set out_c to_take * 0.5
  ;; Conta quanti nodi tra quelli selezionati sono attivi
  ask elements [
    ifelse (is-in-cluster = false) and (x < out_c) [
      set x x + 1
    ]
    [
      set x x + 1
    ]
  ]
  report x / 10
end


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Layouts
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

to layout
 ;; the number 3 here is arbitrary; more repetitions slows down the
 ;; model, but too few gives poor layouts
 repeat layout-repetitions [
 ;; the more turtles we have to fit into the same amount of space,
 ;; the smaller the inputs to layout-spring we'll need to use
 let factor sqrt count turtles
 ;; numbers here are arbitrarily chosen for pleasing appearance
 layout-spring turtles links (1 / factor) (7 / factor) (1 / factor)
 display ;; for smooth animation
 ]
 ;; don't bump the edges of the world
 let x-offset max [xcor] of turtles + min [xcor] of turtles
 let y-offset max [ycor] of turtles + min [ycor] of turtles
 ;; big jumps look funny, so only adjust a little each time
 set x-offset limit-magnitude x-offset 0.1
 set y-offset limit-magnitude y-offset 0.1
 ask turtles [ setxy (xcor - x-offset / 2) (ycor - y-offset / 2) ]
end

;; Function used to initialize globals
to global-initialization
  set total-number-agents count basic-agents
  set neutral-agents count basic-agents with [is-a-active = false and is-b-active = false]
  set active-a-agents count basic-agents with [is-a-active = true]
  set active-b-agents count basic-agents with [is-b-active = true]
  set k count links / count basic-agents
  set total-links count links
  set in-cluster-agents count basic-agents with [is-in-cluster = true]
  set global-cascade false
  set is-warning-active false
  set is-reiterate-active false
end

;; Function used to update globals
to update-globals
  set neutral-agents count basic-agents with [is-a-active = false and is-b-active = false]
  set active-a-agents count basic-agents with [is-a-active = true]
  set active-b-agents count basic-agents with [is-b-active = true]
  set in-cluster-agents count basic-agents with [is-in-cluster = true]
end

;; Function used to intialize agents attributes
to set-characteristics
  set color grey
  set shape "circle"
  set size .5
  set in-degree count my-in-directed-edges
  set out-degree count my-out-directed-edges
  set degree count my-links
  set is-a-active false
  set is-b-active false
  set is-in-cluster false
  set is-active-next false
  set is-inactive-next false
  set received-a-news-counter 0
  set received-b-news-counter 0
  set warning false
  set reiterate false
  set reiterate-counter 0
  set opinion-metric initial-opinion-metric-value
  set is-opinion-b-static false
end

;; Function to setup the network using the Erdős–Rényi model
to ER-RN [N]
  create-basic-agents N [
    setxy random-xcor random-ycor
  ]

  ask basic-agents [
    let x random-normal k-value std-dev
    if x < 0 [
      set x 0
    ]
    ask n-of x basic-agents with [who != [who] of myself] [
      ifelse links-to-use = "undirected" [
         create-undirected-edge-with myself
      ]
      [
         create-directed-edge-to myself
      ]
    ]
  ]
  ask basic-agents [
    set-characteristics
  ]

  ask links [
    set color grey - 1
    set thickness 0.1
  ]

end

;; Function to setup the network using the preferencial attachment model
to P-A
 nw:generate-preferential-attachment basic-agents get-links-to-use nb-nodes 1

  ask basic-agents [
    setxy random-xcor random-ycor
    set-characteristics
  ]
end

;; Funcion to setup the network using the small world model
to S-W

  nw:generate-watts-strogatz basic-agents get-links-to-use nb-nodes neighborhood-size rewire-prob

  ask basic-agents [
    setxy random-xcor random-ycor
    set-characteristics
  ]

end

;; Function used to color agents based on their characteristics
to color-nodes
  ask basic-agents [
    if is-a-active = true [
      set color orange
    ]
    if is-b-active = true [
      set color blue
    ]
    if is-a-active = false and is-b-active = false [
      set color grey
    ]
  ]
  ask super-agents [
    set color violet
  ]
end

;; Function used to setup the inital echo chamber during the setup
to initialize-echo-chamber


  let edges count basic-agents * ( k-value / 2 )

  ;; Calculating the edges where exactly one end is in the echo chamber
  let selected-edges-num (P_N * edges)

  ;; Calculating the number of nodes to insert in the echo chamber
  let c echo-chamber-fraction * count basic-agents

  if c < 0 [
    set c 0
  ]

  ;; Initial nodes that are part of the echo chamber
  ask n-of c basic-agents [
    set is-in-cluster true
  ]


  ;; If the selected edges exceed the maximum number of edges they are set to the total number of edges
  if selected-edges-num > count links [
    set selected-edges-num count links
  ]

  if selected-edges-num < 0 [
    set selected-edges-num 0
  ]


  let mean-connection 0
  ask basic-agents with[is-in-cluster = true][
    let x count link-neighbors with [is-in-cluster = true]
    set mean-connection mean-connection + x
  ]

  ;print(mean-connection)

  ask n-of selected-edges-num links [

    let link-id self

    ;; There is a check to know if exactly one of the two nodes is in the cluster
    ask end1 [
      if breed != super-agents [
        if is-in-cluster = true [
          let node-id self
          ask other-end [
            if breed != super-agents [
              if is-in-cluster = false [
                ;; If exactly one node is in the echo chamber, the link will be removed and replaced with an edge where both nodes belong to the echo chamber
                ask link-id [
                  die
                ]
                ask n-of 1 basic-agents with [who != [who] of node-id and is-in-cluster = true] [
                  ifelse links-to-use = "undirected" [
                    create-undirected-edge-with node-id
                  ][
                    create-directed-edge-to node-id
                  ]
                ]
              ]
            ]
          ]
        ]
      ]
    ]

    ;; The same procedure is repeated by the other side
    ask end2 [
      if breed != super-agents [
        if is-in-cluster = true [
          let node-id self
          ask other-end [
            if breed != super-agents [
              if is-in-cluster = false [
                ;set is-in-cluster-setup  true
                ask link-id [
                  die
                ]
                ask n-of 1 basic-agents with [who != [who] of node-id and is-in-cluster = true] [
                  ifelse links-to-use = "undirected" [
                    create-undirected-edge-with node-id
                  ][
                    create-directed-edge-to node-id
                  ]
                ]
              ]
            ]
          ]
        ]
      ]
    ]
  ]


  ;; The nodes outside the echo chamber have the activation treshold set to teta
  ask basic-agents with [is-in-cluster = false] [
    set activation-treshold teta
  ]

  ;; The nodes inside the echo chamber have the activation treshold set to teta minus the opinion polarization parameter
  ask basic-agents with [is-in-cluster = true] [
    ifelse teta - P_O > 0 [
      set activation-treshold teta - P_O
    ][
      set activation-treshold 0
    ]
  ]

  ;; Before the start of the simulation one node of the echo chamber is set to active with the opinion a
  ask n-of 1 basic-agents with [is-in-cluster = true] [
    set is-a-active true
    ;; We assume that the node has already received an article that supports the opinion a
    set received-a-news-counter received-a-news-counter + 1
    ;; We set a random value to respect the opinion metric relative to the opinion a
    set opinion-metric 0.66 + random-float 0.33

    ;; All the nodes connected to the initial one are set to active
    ask link-neighbors with [breed != super-agents][
      set is-a-active true
      set received-a-news-counter received-a-news-counter + 1
      set opinion-metric 0.66 + random-float 0.33
    ]

  ]


  ask n-of 1 basic-agents with [is-a-active = false and is-in-cluster = false] [
    set is-b-active true
    ;; We assume that the nodes hava already received an article that supports the opinion b
    set received-b-news-counter received-b-news-counter + 1
    ;; We set a random value to respect the opinion metric relative to the opinion b
    set opinion-metric random-float 0.33

    ask link-neighbors with [is-in-cluster = false and breed != super-agents and is-a-active = false][
      set is-b-active true
      set received-b-news-counter received-b-news-counter + 1
      set opinion-metric random-float 0.33
    ]
  ]

  set mean-connection 0
  ask basic-agents with[is-in-cluster = true][
    let x count link-neighbors with [is-in-cluster = true]
    set mean-connection mean-connection + x
  ]

  ;print(mean-connection)

end


to setup-turtles

  ;; Choosing the type of network
  if network = "Erdos Reny" [
     ER-RN nb-nodes
  ]
  if network = "Preferencial Attachment" [
    P-A
  ]
  if network = "Small World" [
    S-W
  ]

  ;; Initialization of basic agents
  ask basic-agents [
    set-characteristics
  ]

  ask links [
    set color grey - 1
    set thickness 0.1
  ]

  ;; Calculating network analysis values
  centrality
  initialize-echo-chamber
  ;; Initializing the super agent
  build-super-agent
  color-nodes

  global-initialization

end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Clusterers
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Function used to detect communities
to community-detection
  carefully [
    let com nw:louvain-communities
    let n-com length com
    (foreach com (range 1 (n-com + 1) 1)[
      [comm c] ->
        ask comm [
          set community c
        ]
    ])
  ][]

end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Centrality Measures
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

to communities
  carefully [
    let com nw:louvain-communities
    let n-com length com
    (foreach com (range 1 (n-com + 1) 1)[
      [comm c] ->
        ask comm [
          set community c
          set color (item (c mod 13) base-colors)
        ]
    ])
    ask patches [set pcolor 3 + [color] of min-one-of basic-agents [distance myself]]
  ]
  []
end

to calculate-grade
  ask basic-agents [
    set in-degree count my-in-directed-edges
    set out-degree count my-out-directed-edges
    set degree count my-links
  ]
end

;; Function used to set centrality measures to each basic agent
to centrality
   ask basic-agents [
    set betweenness nw:betweenness-centrality
    set eigenvector nw:eigenvector-centrality
    set closeness nw:closeness-centrality
    set clustering nw:clustering-coefficient
    set page-rank nw:page-rank
  ]
  calculate-grade
  community-detection

end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Super-Agent
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Function used to create super agent
to build-super-agent
  if sa-active? = true [
    create-super-agents 1 [
      set color violet
      set shape "circle"
      set size .5
    ]
    ;; Choosing between a dynamic super agent or a static one
    ifelse dynamic-sa [
      move-super-agent
    ][
      set-sa-links
    ]
  ]
end

;; Function used to get the first N agents ordered by betweenness
to-report select-by-betweenness

  let node-range-fraction node-range * count basic-agents

  let agent-list sort-on[(- betweenness)] basic-agents
  let result sublist agent-list 0 min list node-range-fraction (length agent-list)

  ;foreach result [
  ; the-basic-agent -> ask the-basic-agent [ show betweeneess]
  ;]

  report turtle-set result

end

;; Function used to get the first N agents ordered by page-rank
to-report select-by-page-rank

  let node-range-fraction node-range * count basic-agents

  let agent-list sort-on[(- page-rank)] basic-agents
  let result sublist agent-list 0 min list node-range-fraction (length agent-list)

  ;foreach result [
   ; the-basic-agent -> ask the-basic-agent [ show page-rank]
  ;]

  report turtle-set result

end

;; Function used to get the first N agents ordered by degree
to-report select-by-degree

  let node-range-fraction node-range * count basic-agents
  let agent-list sort-on[(- degree)] basic-agents
  let result sublist agent-list 0 min list node-range-fraction (length agent-list)
  ;foreach result [
  ;  the-basic-agent -> ask the-basic-agent [ show degree]
  ;]

  report turtle-set result

end

;; Function used to get the first N agents ordered by betweenness
to-report select-by-betweenness-static-b

  let node-range-fraction node-range-static-b * count basic-agents

  let agent-list sort-on[(- betweenness)] basic-agents
  let result sublist agent-list 0 min list node-range-fraction (length agent-list)

  ;foreach result [
  ; the-basic-agent -> ask the-basic-agent [ show betweeneess]
  ;]

  report turtle-set result

end

;; Function used to get the first N agents ordered by page-rank
to-report select-by-page-rank-static-b

  let node-range-fraction node-range-static-b * count basic-agents

  let agent-list sort-on[(- page-rank)] basic-agents
  let result sublist agent-list 0 min list node-range-fraction (length agent-list)

  ;foreach result [
   ; the-basic-agent -> ask the-basic-agent [ show page-rank]
  ;]

  report turtle-set result

end

;; Function used to get the first N agents ordered by degree
to-report select-by-degree-static-b

  let node-range-fraction node-range-static-b * count basic-agents
  let agent-list sort-on[(- degree)] basic-agents
  let result sublist agent-list 0 min list node-range-fraction (length agent-list)
  ;foreach result [
  ;  the-basic-agent -> ask the-basic-agent [ show degree]
  ;]

  report turtle-set result

end

;; Function used to move the super agent during the simulation
to move-super-agent

  ;; The super agent will connect to the node with the max betweenness
  let max-b max [betweenness] of turtles with [breed != super-agents]

  ask basic-agents with [betweenness = max-b] [
    let x xcor
    let y ycor
    ;; Saving the links of the node with max betweenness
    let linked-nodes link-neighbors
    let max-b-node who
    ask super-agents [
      ;; Moving the super agents near the node chosen before
      let x-a x + random 5
      let y-a y + random 5
      ;; Checking if the coordinates respect the limit of the network
      if x-a > max-pxcor [
        set x-a x-a mod max-pxcor
      ]
      if y-a > max-pycor [
        set y-a y-a mod max-pycor
      ]
      setxy x-a y-a

      let sa who
      ;; Deleting the link created before, if there were any
      ask my-links [die]
      ;; Creating a link with the node having the max betweenness
      create-link-with max-b-node
      ;; Connecting the nodes to the super agent
      ask linked-nodes with [who != sa][
        create-link-with myself
      ]
    ]
  ]

  ;; Calculating centrality measures to update the values
  centrality

end

;; Function used to have a static super agent that only create links and does not move in the network
to set-sa-links

  ;; Creating link based on the chosen method
  if choose-method = "betweenness-first" [
    let agents select-by-betweenness
    ask super-agents [
      ask my-links [die]
      ask agents [
        create-undirected-edge-with myself
      ]
    ]
  ]

  if choose-method = "page-rank-first" [
    let agents select-by-page-rank
    ask super-agents [
      ask my-links [die]
      ask agents [
        create-undirected-edge-with myself
      ]
    ]
  ]

  if choose-method = "degree-first" [
    let agents select-by-degree
    ask super-agents [
      ask my-links [die]
      ask agents [
        create-undirected-edge-with myself
      ]
    ]
  ]

  ;; Calculating centrality measures to update the values
  centrality

end

;; Function used to activate the warning procedure for the super agent
to activate-warning

  ;; Setting the global variable
  set is-warning-active true
  ;; Checking if the reitare procedure is already activated
  if is-reiterate-active = false [
    ;; The warning can be of two types, global or non global. The first one is a warning sent to all the basic agents, the second one
    ;; only to the nodes connected to the super agent
    ifelse global-warning = true [
      ask basic-agents [
        set warning true
      ]
    ]
    [
      ifelse dynamic-sa = true [
        move-super-agent
      ][
        set-sa-links
      ]
    ]
  ]
end

;; Function used to activate the reiterate procedure for the super agent
to activate-reiterate
  set is-reiterate-active true
  if is-warning-active = false [
    ifelse dynamic-sa = true [
      move-super-agent
    ][
      set-sa-links
    ]
  ]
end

;; Function used by the super agent to force some agents, chosen by three different criteria, to maintain opinion b till the end of the simulation
to activate-static-b-agents

  if choose-method = "betweenness-first" [
    let agents select-by-betweenness-static-b
    ask agents [
      set is-opinion-b-static true
      set is-inactive-next true
      set opinion-metric 0
    ]
  ]

  if choose-method = "page-rank-first" [
    let agents select-by-page-rank-static-b
    ask agents [
      set is-opinion-b-static true
      set is-inactive-next true
      set opinion-metric 0
    ]
  ]

  if choose-method = "degree-first" [
    let agents select-by-degree-static-b
    ask agents [
      set is-opinion-b-static true
      set is-inactive-next true
      set opinion-metric 0
    ]
  ]
end


;; Function used by the super agent to activate the warning procedure to the nodes connected to it
to warn-agents
  ask super-agents [
    ask link-neighbors [
      set warning true
    ]
  ]
end

;; Function used by the super agent to activate the reiterate procedure to the nodes connected to it
to reiterate-agents
  ask super-agents [
    ask link-neighbors [
      set reiterate true
    ]
  ]
end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Go
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Function used to calculate the global cascade. There is a global cascade when there are more than 50% of basic agents that support the fake news opinion
to calculate-global-cascade
  let active-a-nodes count basic-agents with [is-a-active = true]
  let fraction active-a-nodes / nb-nodes
  ;; Updating the global variable value
  ifelse fraction > 0.5 [
    set global-cascade true
  ] [
    set global-cascade false
  ]

end

;; Function used to know if an agent is about to change opinion based on the opinion metric value. If the opinion metric is between 0.00 and 0.33, the agent
;; will support opinion b. If the opinion metric is between 0.34 and 0.65, the agent will remain neutral and lastly if the value is between 0.66 and 1.00, the agent
;; will support opinion a.
to calculate-opinion-metric [agent opinion]

  ask agent [
    if is-opinion-b-static = false [

      ifelse opinion = "a" [
        ask agent [
          set opinion-metric opinion-metric + opinion-metric-step
          if opinion-metric > 1 [
            set opinion-metric 1
          ]
          if opinion-metric <= 0.33 [
            set is-active-next false
            set is-inactive-next true
          ]
          if opinion-metric >= 0.66 [
            set is-active-next true
            set is-inactive-next false
          ]
          if opinion-metric > 0.33 and opinion-metric < 0.66 [
            set is-active-next false
            set is-inactive-next false
          ]
        ]
      ][
        ask agent [
          set opinion-metric opinion-metric - opinion-metric-step
          if opinion-metric < 0 [
            set opinion-metric 0
          ]
          if opinion-metric <= 0.33 [
            set is-active-next false
            set is-inactive-next true
          ]
          if opinion-metric >= 0.66 [
            set is-active-next true
            set is-inactive-next false
          ]
          if opinion-metric > 0.33 and opinion-metric < 0.66 [
            set is-active-next false
            set is-inactive-next false
          ]
        ]
      ]
    ]
  ]

end

to go

  ;; At the start of the simulation it is checked which procedure the super agent has to do

  ;; If the global warning isn't active, we olny warn the agents connected to the super agent
  if is-warning-active = true and global-warning = false[
    warn-agents
  ]

  ;; If the the reiterate is active the super agent will set "reiterate" to true to the nodes connected to it
  if is-reiterate-active = true [
    reiterate-agents
  ]

  ;; If an agent has changed his opinion toward the fake news in the previous tick, it is set to active with opinion a
  ask basic-agents with [is-active-next = true][
    set is-a-active true
    set is-b-active false
    set is-active-next false
  ]

  ;; If an agent has changed his opinion to not support the fake news in the previous tick, it is set to active with opinion b
  ask basic-agents with [is-inactive-next = true][
    set is-a-active false
    set is-b-active true
    set is-inactive-next false
  ]

  ;; Updating the color of the nodes
  color-nodes

  ask basic-agents [
    let active-a-nodes count link-neighbors with [breed != super-agents and is-a-active = true]
    let active-b-nodes count link-neighbors with [breed != super-agents and is-b-active = true]
    let fraction-a 0
    let fraction-b 0
    if count link-neighbors != 0 [
      ;; Calculating the fraction of active nodes of both opinion
      let fraction count link-neighbors with [breed != super-agents]
      if fraction <= 0 [
        set fraction 1
      ]
      set fraction-a active-a-nodes / fraction
      set fraction-b active-b-nodes / fraction
      ;; If there are more neighbors of the basic agents with opinion a, it will be more likely that he will support opinion a
      if fraction-a > fraction-b [
        ;; Updating the counter of news received
        set received-a-news-counter received-a-news-counter + 1
        ;; If the fraction is greater than the treshold the basic agent will be set to active in the next tick
        if fraction-a > activation-treshold [
          calculate-opinion-metric self "a"

          ;set is-inactive-next false
          ;set is-active-next true
        ]
      ]
      ;; The same thing will happen with the opinion b
      if fraction-b > fraction-a [
        set received-b-news-counter received-b-news-counter + 1
        if fraction-b > activation-treshold [

          calculate-opinion-metric self "b"
          ;set is-active-next false
          ;set is-inactive-next true
        ]
      ]

      if warning = true [

        ;; If the node has already an opinion the warning impact will be less relevant
        if is-a-active = true [
          ;; If the float generated between 0 and 1.00 is less equal than the warning impact, the node will be set no inactive (opinion b) in the next tick
          if random-float 1 <= warning-impact [

            calculate-opinion-metric self "b"
            ;set is-active-next false
            ;set is-inactive-next true
          ]
        ]
        ;; If the node does not have an opinion, the warning will have a more significant impact
        if is-a-active = false and is-b-active = false [
          if random-float 1 <= warning-impact-neutral [

            calculate-opinion-metric self "b"
            ;set is-active-next false
            ;set is-inactive-next true
          ]
        ]
      ]

      if reiterate = true [
        ;; The node, with the variable reitate set to true, will receive another news of type b every tick for each linked neighbor.
        ;; So if the node has 10 linked neighbors, for 10 tick will receive an opinion of type b and will repeat the check on the treshold.
        ifelse reiterate-counter < count link-neighbors with [breed != super-agents] [
          ;; Updating the counter of news b
          set received-b-news-counter received-b-news-counter + 1
          ;; Updating the iterate counter
          set reiterate-counter reiterate-counter + 1
          if random-float 1 <= activation-treshold [
            calculate-opinion-metric self "b"
            ;; If the basic agent has succesfuly changed opinion, the reiterate procedure on it will stop.
            if is-inactive-next = true [
              set reiterate false
              set reiterate-counter 0
            ]
          ]
        ][
          ;; If the counter has reached the number of linked nodes, the reiterate procedure on that node will stop
          set reiterate false
          set reiterate-counter 0
        ]
      ]
    ]
  ]

  ;; If the tick number has not reached the end the simulation will continue
  ifelse ticks < total-ticks [
    tick
    ;; Setting to false the super agent procedures so that they can be activated again in the next ticks
    set is-warning-active false
    set is-reiterate-active false
  ][
    ;; At the end of the simulation the global cascade and global varible values are updated
    calculate-global-cascade
    update-globals
    reset-ticks
    stop
  ]

end
@#$#@#$#@
GRAPHICS-WINDOW
1072
30
1509
468
-1
-1
13.0
1
10
1
1
1
0
0
0
1
-16
16
-16
16
0
0
1
ticks
30.0

SLIDER
8
71
180
104
nb-nodes
nb-nodes
10
10000
100.0
1
1
NIL
HORIZONTAL

BUTTON
207
452
299
527
setup/clear
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

CHOOSER
7
170
145
215
links-to-use
links-to-use
"undirected" "directed"
0

SLIDER
12
298
184
331
P_O
P_O
0
1
0.0
0.01
1
NIL
HORIZONTAL

SLIDER
12
349
184
382
P_N
P_N
0
1
0.2
0.01
1
NIL
HORIZONTAL

SLIDER
205
349
385
382
echo-chamber-fraction
echo-chamber-fraction
0
1
0.2
0.01
1
NIL
HORIZONTAL

SLIDER
205
299
377
332
teta
teta
0
1
0.27
0.001
1
NIL
HORIZONTAL

BUTTON
307
452
397
527
NIL
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
266
125
438
158
k-value
k-value
0
20
8.0
1
1
NIL
HORIZONTAL

CHOOSER
266
72
448
117
network
network
"Erdos Reny" "Preferencial Attachment" "Small World"
0

SLIDER
468
125
640
158
rewire-prob
rewire-prob
0
1
0.3
0.01
1
NIL
HORIZONTAL

SLIDER
469
176
641
209
neighborhood-size
neighborhood-size
1
100
4.0
1
1
NIL
HORIZONTAL

SLIDER
266
174
438
207
std-dev
std-dev
0
50
2.0
1
1
NIL
HORIZONTAL

SWITCH
8
121
111
154
layout?
layout?
0
1
-1000

SLIDER
12
489
184
522
total-ticks
total-ticks
10
1000
100.0
1
1
NIL
HORIZONTAL

SWITCH
462
296
580
329
dynamic-sa
dynamic-sa
1
1
-1000

TEXTBOX
489
263
639
281
Super Agent
11
0.0
1

TEXTBOX
15
270
165
288
Simulation parameters
11
0.0
1

TEXTBOX
13
27
163
45
Network attributes
11
0.0
1

SWITCH
597
297
709
330
sa-active?
sa-active?
0
1
-1000

BUTTON
464
346
589
379
NIL
activate-warning
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
605
346
734
379
NIL
activate-reiterate
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
465
397
610
430
warning-impact
warning-impact
0
1
0.5
0.01
1
NIL
HORIZONTAL

MONITOR
466
550
586
595
NIL
get-a-active-agents
17
1
11

MONITOR
467
601
585
646
NIL
get-neutral-agents
17
1
11

MONITOR
597
600
721
645
NIL
get-b-active-agents
17
1
11

SLIDER
623
397
777
430
warning-impact-neutral
warning-impact-neutral
0
1
0.5
0.01
1
NIL
HORIZONTAL

SLIDER
465
436
609
469
node-range
node-range
0
1
0.1
0.01
1
NIL
HORIZONTAL

CHOOSER
624
479
773
524
choose-method
choose-method
"betweenness-first" "page-rank-first" "degree-first"
0

SLIDER
115
121
229
154
layout-repetitions
layout-repetitions
1
20
10.0
1
1
NIL
HORIZONTAL

SWITCH
465
479
609
512
global-warning
global-warning
0
1
-1000

SLIDER
12
395
187
428
initial-opinion-metric-value
initial-opinion-metric-value
0
1
0.5
0.01
1
NIL
HORIZONTAL

SLIDER
12
442
187
475
opinion-metric-step
opinion-metric-step
0
1
1.0
0.01
1
NIL
HORIZONTAL

BUTTON
745
346
889
379
NIL
activate-static-b-agents
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
596
549
725
594
NIL
get-in-cluster-agents
17
1
11

BUTTON
493
73
591
106
NIL
communities\n
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
622
437
779
470
node-range-static-b
node-range-static-b
0
1
0.05
0.01
1
NIL
HORIZONTAL

@#$#@#$#@
## WHAT IS IT?

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.4.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="experiment" repetitions="100" runMetricsEveryStep="false">
    <setup>reset-ticks
setup</setup>
    <go>go</go>
    <metric>get-cascade</metric>
  </experiment>
</experiments>
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
