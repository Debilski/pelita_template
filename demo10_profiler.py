# This bot shows how to enable a debugger session to explore the objects
# IMPORTANT: timeouts need to be disabled, or you will not have time to use
# the debugger at all. Run a game with:
# pelita --no-timeout demo08_debugger.py demo01_stopping.py
#

from demo04_basic_attacker import move as attacking_move

TEAM_NAME = 'Profiler Bot'

@profile
def move(bot, state):
    next_move, state = attacking_move(bot, state)
    return next_move, state

if __name__ == '__main__':
    import pelita
    layout_name, layout_string = pelita.layout.get_random_layout(filter="normal")
    pelita.libpelita.run_game([move, "demo05_basic_defender.py"], rounds=300, layout=layout_string)
