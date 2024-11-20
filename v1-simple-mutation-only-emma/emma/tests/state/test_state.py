import unittest
from state.shared_state import shared_state

class TestStateFunctions(unittest.TestCase):
    def test_shared_state_flags(self):
        self.assertFalse(shared_state.STOP_FLAG)
        self.assertFalse(shared_state.PAUSE_FLAG)

if __name__ == '__main__':
    unittest.main()
