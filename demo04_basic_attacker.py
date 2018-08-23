# This bot picks a food pellet at random, then goes and tries to get it.
# It tries on the way to avoid being eaten by the enemy: if the next move
# to get to the food would put it on a enemy bot in its own homezone, then
# it steps back to its previous position
TEAM_NAME = 'Basic Attacker Bots'

from pelita.graph import Graph

from utils import next_step

def move(turn, game):
    bot = game.team[turn]

    # we need to create a dictionary to keep information
    # over turns for each individual bot
    # - we want to track previous positions, so that we can backtrack if needed
    # - we want to keep track of the food pellet we are aiming at the moment
    if game.state is None:
        # initialize a state dictionary
        game.state = {}
        # each bot needs its own state dictionary to keep track of the
        # food targets
        game.state[0] = None
        game.state[1] = None
        # initialize a graph representation of the maze
        game.state['graph'] = Graph(bot.position, bot.walls)

    # if we don't have a target food pellet, choose one at random now
    if game.state[turn] is None:
        game.state[turn] = bot.random.choice(bot.enemy[0].food)

    # did we (or the other bot) eat our target already?
    if game.state[turn] not in bot.enemy[0].food:
        # let's choose one random food pellet as our new goal
        game.state[turn] = bot.random.choice(bot.enemy[0].food)

    # get the next position along the path to reach our target food pellet
    next_pos = next_step(bot.position,
                         game.state[turn],
                         game.state['graph'])

    # now, let's check if we are getting too near to our enemy
    # where are the enemy ghosts?
    for enemy_pos in (bot.enemy[0].position, bot.enemy[1].position):
        if (next_pos == enemy_pos) and (next_pos not in bot.homezone):
            # we are in the enemy zone: they can eat us!
            # let us just step back
            try:
                next_pos = bot.track[-2]
            except IndexError:
                # we can't go 2 steps back (we have been eaten or who knows why)
                # let's just stop
                next_pos = bot.position
            # let's forget about this food pellet for now and wait for next
            # move to choose another one
            game.state[turn] = None

    return bot.get_move(next_pos)
