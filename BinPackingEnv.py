from typing import Tuple
import math
import pygame

class BinPackingEnv():
    RW_VALID = 1 # reward given for valid placement
    PN_INVALID = -1 # penalty for invalid placement (scaled on how much overlap?)

    def __init__(self, circles: list):
        self.circles = circles # List of circle radiis. ex: [r1, r2, r3]
        self.placed_circles = list() # List of positions of placed circles and their radii. ex: [(x, y), r]
        self.circles_left = len(self.circles) - len(self.placed_circles)
        self.num_circles = len(circles)
        self.num_circles_left = len(self.circles)
        self.current_index = 0
        self.done = False
        print("Bin initialized.")


    def reset(self) -> Tuple[list, int]:
        # Empties the bin and resets index, returns the new (empty) state.
        self.placed_circles = list()
        self.current_index = 0
        self.done = False
        return self._get_state()
    
    def _get_state(self) -> Tuple[list, int]:
        # returns the state (positions of placed circles, index)
        return self.placed, self.index
    
    def step(self, action: tuple) -> Tuple[list, int, int, type]:
        # Takes in the action (position). ex: action = (x, y)
        # Returns the next state, reward/penalty, and status, based on the validity of the action.
        reward = 0
        if self._is_valid_placement(action, self.circles[self.index]):
            reward += self.RW_VALID
        else:
            reward += self.PN_INVALID
        
        self.index += 1
        if self.index == self.num_circles:
            self.done = True

        return self._get_state(), reward, self.done


    def _is_valid_placement(self, position, radius) -> type:
        # Determines validity of position with radius given already packed circles.
        if position[0] < radius or position[1] < radius:
            return False
        for taken_pos, taken_r in self.placed_circles:
            if math.dist(taken_pos, position) <= taken_r + radius:
                return False
        return True
