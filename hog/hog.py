"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1


    score_roll = 0
    whether_roll_1 = True #To show whether the number of this roll is 1
    for i in range(1,num_rolls + 1):
        x = dice()
        if x == 1:
            whether_roll_1 = False

        else:
            score_roll = score_roll + x
    if whether_roll_1 == True:
        return score_roll
    else:
        return 0

    # END Question 1


from math import ceil
def next_prime(x): #The function to get next prime number that is bigger than x
    while x > 0:
        prime_or_not= True #To show whether number x has a factor
        x = x + 1
        for i in range(2, ceil(x/2)+1):
            if x % i == 0:
                prime_or_not = False
                break
        if prime_or_not == True:
            return x
def is_prime(x): #To showthat current number x is a prime number
    prime_or_not = True
    if x == 1:
        return False
    elif x == 0:
        return False
    for l in range(2, ceil(x/2)+1):
        if x%l == 0:
            prime_or_not = False
            break
    return prime_or_not
def large_digit(x): #To get the largest digit of opponent score
    m = x // 10
    x = x % 10
    return max(m,x)

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2

    s = 0
    if num_rolls == 0:
        m = large_digit(opponent_score)+1
        if is_prime(m) == True:
            m = next_prime(m)
    else:
        m = roll_dice(num_rolls, dice)
        if is_prime(m) == True:
            return next_prime(m)
    return m


    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    if score0 %100 == (score1 % 10)*10 + (score1 // 10) % 10:
        return  True
    else:
        return False
    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5


    while score0 <goal and score1<goal:
        if who == 0:
            dice_this_turn = select_dice(score0, score1) #To decide what dice to use in this turn
            s0 = strategy0(score0, score1)
            score_this_turn = take_turn(s0, score1, dice_this_turn)
            if score_this_turn == 0:
                score1 = score1 + s0
            else:
                score0 = score0 + score_this_turn

            if is_swap (score0, score1) == True:
                score0, score1 = score1, score0
            who = other(who)
        else:
            dice_this_turn = select_dice(score1, score0) #To decide what dice to use in this turn
            s1 = strategy1(score1, score0)
            score_this_turn = take_turn(s1, score0, dice_this_turn)

            if score_this_turn == 0:
                score0 = score0 + s1
            else:
                score1 = score1 + score_this_turn
            if is_swap (score0, score1) == True:
                score0, score1 = score1, score0
            who = other(who)


    # END Question 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def print_and_return(*args):
        result = 0
        for i in range(1, num_samples + 1):
            result = result + fn(*args)
        return result / num_samples
    return print_and_return


    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    num_dice = 1
    max =  make_averaged(roll_dice, num_samples)(1, dice)
    for i in range(2, 11):
        new_average_score = make_averaged(roll_dice, num_samples)(i, dice)
        if   max < new_average_score:
            num_dice, max = i, new_average_score
    return num_dice
    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8

    def large_digit(x): #To get the largest digit of opponent score
        m = x // 10
        x = x % 10
        return max(m,x)
    if margin <= large_digit(opponent_score)+1:
        return 0
    elif is_prime(large_digit(opponent_score)+1) == True:
        if next_prime(large_digit(opponent_score)+1) >= margin:
            return 0
    else:
        return num_rolls
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    def large_digit(x): #To get the largest digit of opponent score
        m = x // 10
        x = x % 10
        return max(m,x)

    if score < opponent_score: #The suitable situation for using swap_strategy
        if is_swap(large_digit(opponent_score)+1+score , opponent_score) == True:
            if large_digit(opponent_score)+1+score == opponent_score:
                return num_rolls
            else:
                return 0
        else:
            if is_prime(large_digit(opponent_score)+1) == True:
                if is_swap(next_prime(large_digit(opponent_score)+1)+score , opponent_score) == True:
                    if next_prime(large_digit(opponent_score)+1)+score == opponent_score:
                        return num_rolls
                    else:
                        return 0
                else:
                    return num_rolls
            else:
                return num_rolls
    else:
        return(num_rolls)

    # END Question 9


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    If using free_bacon strategy can push the opponent player into Hog Wild, then we use free_bacon to increase opponent's chance of rolling 1.
    In other conditions, if free_bacon allows us to score more than swap_strategy, we use free_bacon. Otherwise, we use swap_strategy.
    If using free_bacon and swap_strategy gets the current player the same scores, the program uses free bacon because it's safer.
    The margin is set to 2 because after certain calculation, the expected value of scores we get from one dice is between 2 and 3.
    The num_rolls is set as 4 because the expected value of rolling multiple dice reaches highest when rolling 4 dice (if we calculate rolling "1" as losing one point to opponent).
    """
    # BEGIN Question 10
    a = bacon_strategy(score, opponent_score, margin = 2, num_rolls = 4)
    b = swap_strategy(score, opponent_score, num_rolls= 4)
    if is_prime(large_digit(opponent_score)+1) == True:
        if (next_prime(large_digit(opponent_score)+1) +score + opponent_score)  % 7  == 0:
            return 0
        else:
            return bacon_strategy(score, opponent_score, margin = 2, num_rolls = 4)

    elif (large_digit(opponent_score)+1 + score + opponent_score) % 7 == 0:
        return 0
    elif a <= b:
        return a
    else:
        return b



    # END Question 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
