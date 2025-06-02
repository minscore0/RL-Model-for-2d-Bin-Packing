class BinPackingEnv():
    def __init__(self, circles: list):
        self.circles = circles # List of circle radiis
        self.num_circles = len(circles)
        self.circles_left = len(self.circles)
        self.placed = list()
        self.current_index = 0
        self.done = False
        print("Bin initialized.")

    def reset(self):
        # Empties the bin and resets index, returns the new (empty) state.
        self.placed_circles = list()
        self.current_index = 0
        self.done = False
        return self._get_state()
    
    def _get_state(self):
        # returns the state (positions of placed circles, index)
        pass
    
    def step(self, action: tuple):
        # Returns the next state, reward/penalty, and status, based on the validity of the action.
        pass

    def _is_valid_placement(self, position, radius):
        # Determines validity of position with radius given already packed circles.
        pass

