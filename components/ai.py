from __future__ import annotations

from typing import List, Tuple

import numpy as np
import tcod

from actions import Action
from components.base_component import BaseComponent

class BaseAI(Action, BaseComponent):
    def perform(self) -> None:
        raise NotImplementedError
    
    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position
        
        If there is no valid path then returns an empty list
        """
        
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)
        
        for entity in self.entity.gamemap.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10
                
        # create a graph from the cost array and pass that graph to a new pathfinder
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)
        
        pathfinder.add_root((self.entity.x, self.entity.y)) # Start Position
        
        # Compute the path to the destination and remove the starting point
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()
        
        # Convert from list to list
        return [(index[0], index[1]) for index in path]