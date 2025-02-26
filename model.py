import mesa
import networkx as nx
import numpy as np  
from mesa.time import RandomActivation  # Agent scheduler
from tqdm import tqdm  # Progress bar for simulation steps

class Population(mesa.Model):
    """ 
    Represents the simulation environment with bacteria moving through the city.
    """

    def __init__(self, num_steps, num_agents, graph, seed=None):
        """
        Initializes the simulation with bacteria agents and a road network.
        
        Parameters:
        - num_steps: Number of steps in the simulation.
        - num_agents: Number of bacteria.
        - graph: The road network.
        - seed: whatever.
        """
        super().__init__(seed=seed)
        self.num_steps = num_steps
        self.num_agents = num_agents
        self.graph = graph  #road network from map.py
        self.schedule = RandomActivation(self)  # Scheduler to randomly activate agents
        self.running = True  

    def init_agents(self):
        """ Initializes bacteria at random locations on the road network. """
        nodes = list(self.graph.nodes)  # Get all intersections (nodes)
        for i in range(self.num_agents):
            start_node = self.random.choice(nodes)  # Pick a random intersection
            agent = Bacteria(i, self, start_node)  # Create an agent
            self.schedule.add(agent)  # Add agent to scheduler

    def step(self):
        """ Advances the simulation by one step (moves all agents). """
        self.schedule.step()

    def run(self):
        """ Runs the simulation for a set number of steps. """
        for _ in tqdm(range(self.num_steps)):  
            self.step()

class Bacteria(mesa.Agent):
    """
    Represents a bacteria moving randomly through the road network.
    """

    def __init__(self, unique_id, model, start_node):
        """
        Initializes a bacteria agent at a given intersection.
        
        Parameters:
        - unique_id: A unique identifier for the agent.
        - model: The simulation model (Population).
        - start_node: The initial location (intersection) of the bacteria.
        """
        super().__init__(unique_id, model)
        self.node = start_node  # Current intersection

    def get_neighbors(self):
        """ Returns neighboring intersections (nodes) the bacteria can move to. """
        return list(self.model.graph.neighbors(self.node))

    def move(self):
        """ Moves the bacteria randomly to a neighboring intersection. """
        neighbors = self.get_neighbors()
        if neighbors:
            self.node = self.random.choice(neighbors)  # Pick a random intersection

    def step(self):
        """ Executes one movement step per simulation step. """
        self.move()

