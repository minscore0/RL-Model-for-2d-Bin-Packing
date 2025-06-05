from typing import Tuple
import math
import pygame

class BinPackingEnv():
    RW_VALID = 1 # reward given for valid placement
    PN_INVALID = -1 # penalty for invalid placement (scaled on how much overlap?)

    def __init__(self, circle_radii: list):
        self.circle_radii = circle_radii # List of circle radii. ex: [r1, r2, r3]
        self.circles = [[r, [0, 0]] for r in self.circle_radii] # List of positions of placed circles and their radii. ex: [r, [x, y]]
        self.num_circles = len(self.circle_radii)
        self.index = 0
        self.placed_circles = self.circles[:self.index]
        self.done = self.index == self.num_circles
        print("Bin initialized.")

    def reset(self) -> Tuple[list, int]:
        # Empties the bin and resets index, returns the new (empty) state.
        self.placed_circles = [[r, [0, 0]] for r in self.circle_radii]
        self.index = 0
        self.done = False
        return self.get_state()
    
    def get_state(self) -> Tuple[list, int]:
        # returns the state (positions, index)
        return self.circles, self.index
    
    def step(self, action: tuple) -> tuple[tuple[list, int], int]:
        # Takes in the action (position). ex: action = (x, y)
        # Returns the next state, reward/penalty, and status, based on the validity of the action.
        reward = 0
        if self.is_valid_placement(action, self.circles[self.index]):
            reward += self.RW_VALID
        else:
            reward += self.PN_INVALID

        self.circles[self.index][1] = action
        self.index += 1
        if self.index == self.num_circles:
            self.done = True

        return self.get_state(), reward

    def is_valid_placement(self, position, radius) -> bool:
        # Determines validity of position with radius given already packed circles.
        if position[0] < radius or position[1] < radius:
            return False
        for taken_pos, taken_r in self.placed_circles:
            if math.dist(taken_pos, position) <= taken_r + radius:
                return False
        return True
