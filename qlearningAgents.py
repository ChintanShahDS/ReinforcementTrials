# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        ## Initialize as Counter that is extended from dictionary
        self.qvalues = util.Counter()
        # print("Qvalues at init:", self.qvalues)

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # print("Qvalues at getQValue:", self.qvalues[(state, action)])
        # These return the qValues for a particular state and action
        return self.qvalues[(state, action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # Return the max qvalue out of the 4 used for calculations in update
        legal_actions = self.getLegalActions(state)

        # print("legal_actions:", legal_actions)
        if legal_actions:
            # print("computeValueFromQValues legal_actions:", [self.getQValue(state, a) for a in legal_actions])
            # print("self.qvalues:", self.qvalues)
            return max([self.getQValue(state, a) for a in legal_actions])
        else:
            return 0.0

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # Return the action and the qvalue chosen based on the current state and and the max of the Qvalue
        # Used in getAction to determine the action

        legal_actions = self.getLegalActions(state)

        # print("legal_actions:", legal_actions)
        if not legal_actions:
            return None

        action_QValue_pairs = [(a, self.getQValue(state, a)) for a in legal_actions]
        # print("action_QValue_pairs:", action_QValue_pairs)
        max_pair = max(action_QValue_pairs, key=lambda x: x[1])
        # print("max_pair:", max_pair)
        return max_pair[0]


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        # Here a random_action is chosen from the list of legalActions in that position for some times
        # Else the action is chosen based on Policy that is based on the Max
        # This is to ensure that it is more explorative
        # This is called as a callback for making a decision on the action to be taken in gridworld.py
        random_action = util.flipCoin(self.epsilon)
        # print("random_action:", random_action)

        if legalActions:
          if random_action:
              action = random.choice(legalActions)
          else:
              action = self.getPolicy(state)

        print("getAction action:", action)
        return action


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # This actually updates the qValues using the formula for QLearning
        # Called by environment during every transition
        # SAMPLE:  sample = R(s, a, s') + gamma max_a' Q(s', a')
        # UPDATE:  Q(s, a) = (1 - alpha) Q(s, a) + alpha [sample]
        R = reward
        max_Q = self.getValue(nextState)
        gamma = self.discount
        Q = self.qvalues[(state, action)]

        sample = R + gamma * max_Q
        self.qvalues[(state, action)] = (1 - self.alpha) * Q + self.alpha * sample
        print("update Reward:", R, "max_Q:", max_Q, "gamma:", gamma, "Q:", Q, "sample:", sample)
        print("state:", state, "action:", action, "self.qvalues[(state, action)]:", self.qvalues[(state, action)])

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
