import random
from enum import IntEnum
import sys
import argparse
import math

class Card:
    def __init__(self, color, rank, value):
        self.color = color
        self.rank = rank
        self.value = value
        
    def __str__(self):
        return self.rank + " of " + self.color
        
    def __eq__(self, other):
        return self.color == other.color and self.rank == other.rank

def generate_deck(suits=["Hearts", "Spades", "Clubs", "Diamonds"], 
                  ranks=[("2",2), ("3",3), ("4",4), ("5",5), ("6",6), ("7",7), ("8",8), ("9",9), ("10",10), ("Jack",10), ("Queen",10), ("King",10), ("Ace",11)]):
    result = []
    for suit in suits:
        for (rank,value) in ranks:
            result.append(Card(suit,rank,value))
    return result
    
def format(cards):
    if isinstance(cards, Card):
        return str(cards)
    return ", ".join(map(str, cards))
    
def get_value(cards):
    """
    Calculate the value of a set of cards. Aces may be counted as 11 or 1, to avoid going over 21
    """
    result = 0
    aces = 0
    for c in cards:
        result += c.value
        if c.rank == "Ace":
            aces += 1
    while result > 21 and aces > 0:
        result -= 10
        aces -= 1
    return result
    

class PlayerType(IntEnum):
    PLAYER = 1
    DEALER = 2
    
class Action(IntEnum):
    HIT = 1
    STAND = 2
    DOUBLE_DOWN = 3
    SPLIT = 4

class Player:
    """
    The basic player just chooses a random action
    """
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
    def get_action(self, cards, actions, dealer_cards):
        return random.choice(actions)
    def reset(self):
        pass
        
class TimidPlayer(Player):
    """
    The timid player always stands, and never takes additional cards.
    """
    def get_action(self, cards, actions, dealer_cards):
        return Action.STAND
        
class BasicStrategyPlayer(Player):
    """
    Basic strategy: If the dealer has a card lower than a 7 open, we hit if we have less than 12. Otherwise, we hit if we have less than 17. The idea being: If the dealer has a low card open, they are more likely to bust, if they have a high card open they are more likely to stand with a high score that we need to beat.
    """
    def get_action(self, cards, actions, dealer_cards):
        pval = get_value(cards)
        if dealer_cards[0].value < 7:
            if pval < 12:
                return Action.HIT 
            return Action.STAND 
        if pval < 17:
            return Action.HIT
        return Action.STAND
        
MCTS_N = 500
"""
 class MCTSPlayer(Player):
    
    This is only a demonstration, not *actual* Monte Carlo Tree Search!
    
    This agent will run MCTS_N simulations. For each simulation, the cards the player has not yet seen are shuffled and used as the assumed deck. Then the `RolloutPlayer` plays MCTS_N games starting from that random shuffle 
    The agent will only remember the *first* action taken by the `RolloutPlayer` and how many points where obtained 
    on average for each possible action.
    
    def __init__(self, name, deck):
        self.name = name
        self.bet = 2
        self.deck = deck
    def get_action(self, cards, actions, dealer_cards):
        
        # Make a copy of the deck!
        deck = self.deck[:]
        
        # Remove cards we have already seen (ours, and the open dealer card)
        for p in cards:
            deck.remove(p)
        for p in dealer_cards:
            deck.remove(p)
        
        # For each of our simulations we use the rollout player. 
        # Our Rollout Player selects actions at random, and records what it did (!)
        p = RolloutPlayer("Rollout", deck)# need to make a tree here and it needs to know if it needs to expand nodes or not
        p.initTree(cards,dealer_cards)
        # We create a new game object with the reduced deck, played by our rollout player
        g1 = Game(deck, p, verbose=False)
        results = {}
        for i in range(MCTS_N):#note this is looped 100 times
            #print("FOR GAME STATE: " ,get_value(cards), get_value(dealer_cards))
            
            # The rollout player stores its action history, we reset this first
            p.reset()
            
            # continue_round allows us to pass a partial game state (which cards we have, what the open 
            # card of the dealer is, and how much we've bet), and continue the game from there 
            # i.e. the game will *not* deal us two new cards, but instead use the ones we already have 
            # It will, however, then run as normal, calling `get_action` on the player object we passed earlier,
            # which is our rollout_player
            # The return value is the amount of money the agent won, across *all* hands (if they split)
            res = g1.continue_round(cards, dealer_cards, self.bet)
            
            # After we are done, we extract the first action we took
            act = p.actions[0]
            #print(act, res)
            # Record the result for each possible action
            if act not in results:
                results[act] = []
            results[act].append(res)
        
        # Calculate the action with the highest *average* return
        max = -1000
        act = Action.STAND
        avgs = {}
        for a in results:
            score = sum(results[a])*1.0/len(results[a])
            avgs[a] = score
            if score > max:
                max = score
                act = a
                
        # Make sure we also record our own bet in case we double down (!)
        if act == Action.DOUBLE_DOWN:
            self.bet *= 2
        return act
    def reset(self):
        self.bet = 2
"""        
class MCTSPlayer(Player):
    """
    This is only a demonstration, not *actual* Monte Carlo Tree Search!
    
    This agent will run MCTS_N simulations. For each simulation, the cards the player has not yet seen are shuffled and used as the assumed deck. Then the `RolloutPlayer` plays MCTS_N games starting from that random shuffle 
    The agent will only remember the *first* action taken by the `RolloutPlayer` and how many points where obtained 
    on average for each possible action.
    """
    def __init__(self, name, deck):
        self.name = name
        self.bet = 2
        self.deck = deck
    def get_action(self, cards, actions, dealer_cards):
        
        # Make a copy of the deck!
        deck = self.deck[:]
        
        # Remove cards we have already seen (ours, and the open dealer card)
        for p in cards:
            deck.remove(p)
        for p in dealer_cards:
            deck.remove(p)
        
        # For each of our simulations we use the rollout player. 
        # Our Rollout Player selects actions at random, and records what it did (!)
        p = RolloutPlayer("Rollout", deck)# need to make a tree here and it needs to know if it needs to expand nodes or not
        p.initTree(cards,dealer_cards)
        # We create a new game object with the reduced deck, played by our rollout player
        g1 = Game(deck, p, verbose=False)
        results = {}
        
        for i in range(MCTS_N):#note this is looped 100 times
            p.reset()
            res = g1.continue_round(cards, dealer_cards, self.bet)
            #if p.myTree.hasSplitNode:
                #print("Made it back!")
            #print(p.myTree.currentNode.values)
            #print(p.myTree.currentNode.values)
            p.myTree.currentNode.values.append(res)
            #print(p.myTree.currentNode.values,p.myTree.currentNode.timesVisited)
            #print()
            temp = p.myTree.currentNode.parent
            """
            Back propogate results to master nodes off root and increment
            """
            while temp is not p.myTree.rootNode and temp is not None:
                temp.values.append(res)##will have to back propogate here
                #temp.timesVisited = temp.timesVisited + 1
                temp = temp.parent
        """
        Calculate best average to return
        """
        splitScore = -100
        split = None
        if p.myTree.hasSplitNode == True:
            split = p.myTree.rootNode.splitNode
            splitScore = (sum(split.values)/split.timesVisited)
        hit = p.myTree.rootNode.hitNode
        #print(hit.values, hit.timesVisited)
        stand = p.myTree.rootNode.standNode
        dd = p.myTree.rootNode.ddNode
        #print(stand.values, stand.timesVisited)
        #print(dd.values, dd.timesVisited)
        hitScore =(sum(hit.values)/hit.timesVisited)
        standScore = (sum(stand.values)/stand.timesVisited)
        ddScore = (sum(dd.values)/dd.timesVisited)
        
        max = hitScore
        act = Action.HIT
        if standScore > hitScore:
            max = standScore
            act = Action.STAND
        if ddScore > (standScore and hitScore):
            max = ddScore
            act = Action.DOUBLE_DOWN
        if splitScore > (standScore and hitScore and ddScore):
            max = splitScore
            act = Action.SPLIT
        #print("Root Node values: ",p.myTree.rootNode.values)
        """
        print("Hit Node : ",p.myTree.rootNode.hitNode.values, "Times Visited:" , p.myTree.rootNode.hitNode.timesVisited, "Average: ", hitScore) 
        print("Stand Node values: ",p.myTree.rootNode.standNode.values, "Times Visited:" , p.myTree.rootNode.standNode.timesVisited, "Average: ", standScore)
        print("Double Down Node values: ",p.myTree.rootNode.ddNode.values, "Times Visited:" , p.myTree.rootNode.ddNode.timesVisited, "Average: ", ddScore)
        
        print("Hit Node : ", "Times Visited:" , p.myTree.rootNode.hitNode.timesVisited, "Average: ", hitScore) 
        print("Stand Node values: ", "Times Visited:" , p.myTree.rootNode.standNode.timesVisited, "Average: ", standScore)
        print("Double Down Node values: " "Times Visited:" , p.myTree.rootNode.ddNode.timesVisited, "Average: ", ddScore)
        """
        #print("Split Node values: ",p.myTree.rootNode.splitNode.values)
        # Make sure we also record our own bet in case we double down (!)
        if act == Action.DOUBLE_DOWN:
            self.bet *= 2
        #print(act)
        return act
    def reset(self):
        self.bet = 2
 
"""
Create Tree Structure
"""
class MCTSTree:
    def __init__(self):
        self.hasRoot = False
        self.rootNode = None
        self.currentNode = None
        self.hasSplitNode = False
        self.inSplit = False
        self.isTraversing = False
"""
Create Node Structure to use with tree
"""
class MCTSNode: #current game state
    def __init__(self, cards, dealer_cards):
        """
        Cards of Node
        """
        self.pcards = cards #our card value in current state
        self.dcards = dealer_cards
        self.handValue = get_value(cards)
        """
        Node properties
        """
        
        self.name = None
        self.parent = None
        self.isLeaf = False
        
        self.hitNode = None
        self.hitNodeExpected = 0
        
        self.standNode = None
        self.standNodeExpected = 0
        
        self.ddNode = None
        self.ddNodeExpected = 0
        
        self.splitNode = None
        self.splitNodeExpected = 0
        
        self.timesVisited = 0
        self.values = []         
    def printNode(self):
        print("Current state: ")
        print("Player value is:",self.pcards,"Dealer Value is: ",self.dcards,"Parent is :", self.parent)
        
class RolloutPlayer(Player):
    #if all actions are expanded use selection strategy
    #if not all actions are expanded choose one and expand it
    def __init__(self, name, deck):
        self.name = name
        self.actions = []
        self.deck = deck
        #Initialize tree
        self.myTree = MCTSTree()
    def initTree(self,cards,dealer_cards):
            node = MCTSNode(cards,dealer_cards)
            node.name = "root"
            self.myTree.rootNode = node
            self.myTree.parent = node
            self.myTree.hasRoot = True
            self.myTree.currentNode = node        
    def get_action(self, cards, actions, dealer_cards):
        """Expand unexpanded"""
        tree = self.myTree
        if tree.inSplit:
            #print("playing random for split")
            act = random.choice(actions)
            #act = self.selection()
            self.actions.append(act)
            return act
        #first expand each path
        splitAvail=False
        """
        First Expands all available nodes if node is not a leaf
        Split is only available from root node(since we have 2 cards in that state)
        
        The current node is used,
        """
        if len(cards) == 2 and same_value(cards[0], cards[1]) and (tree.currentNode is tree.rootNode):
            splitAvail= True
        if tree.rootNode.splitNode is None and splitAvail and tree.hasSplitNode == False:
            #print("INSIDE THE SPLIT NODE!!!")
            tree.rootNode.splitNode = MCTSNode(tree.rootNode.pcards,tree.rootNode.dcards) #make a new node
            tree.rootNode.splitNode.parent = tree.rootNode#update nodes parent
            tree.currentNode = tree.rootNode.splitNode #update current node selection            
            tree.currentNode.timesVisited = tree.currentNode.timesVisited + 1
            tree.currentNode.isLeaf = True
            tree.hasSplitNode = True
            act = Action.SPLIT
            self.actions.append(act)
            tree.inSplit = True
            #print("Made it to end of SPlit Function")
            return act
        if tree.currentNode.standNode is None and (tree.currentNode.isLeaf == False):
            #print("INSIDE THE STAND NODE!!!")
            tree.currentNode.standNode = MCTSNode(tree.currentNode.pcards,tree.currentNode.dcards) #make a new node
            tree.currentNode.standNode.parent = tree.currentNode#update nodes parent
            tree.currentNode = tree.currentNode.standNode #update current node selection            
            tree.currentNode.timesVisited = tree.currentNode.timesVisited + 1
            tree.currentNode.isLeaf = True
            act = Action.STAND
            self.actions.append(act)
            return act
            print("After return for stand")
        if tree.currentNode.ddNode is None and (tree.currentNode.isLeaf == False) :
            #print("INSIDE THE DD NODE!!!")
            tree.currentNode.ddNode = MCTSNode(tree.currentNode.pcards,tree.currentNode.dcards) #make a new node
            tree.currentNode.ddNode.parent = tree.currentNode#update nodes parent
            tree.currentNode = tree.currentNode.ddNode #update current node selection            
            tree.currentNode.timesVisited = tree.currentNode.timesVisited + 1
            tree.currentNode.isLeaf = True
            act = Action.DOUBLE_DOWN
            self.actions.append(act)
            return act
        if (tree.currentNode.hitNode is None) and (tree.currentNode.isLeaf == False):
            #print("INSIDE THE HIT NODE!!!")
            tree.currentNode.hitNode = MCTSNode(tree.currentNode.pcards,tree.currentNode.dcards) #make a new node
            myDeck = self.deck
            random.shuffle(myDeck)
            nextCard = myDeck[0]
            #print(nextCard)
            #print(get_value(tree.currentNode.hitNode.pcards))
            #tree.currentNode.hitNode.pcards.append(nextCard)
            tree.currentNode.hitNode.handValue = tree.currentNode.handValue + nextCard.value
            #print(get_value(tree.currentNode.hitNode.pcards))
            #if get_value(tree.currentNode.hitNode.pcards) >= 21:
            if tree.currentNode.hitNode.handValue >= 21:
                tree.currentNode.hitNode.isLeaf = True
                #tree.currentNode.hitNode.pcards.pop()#remove busted card and mark as leaf
            tree.currentNode.hitNode.parent = tree.currentNode#update nodes parent
            tree.currentNode = tree.currentNode.hitNode #update current node selection            
            tree.currentNode.timesVisited = tree.currentNode.timesVisited + 1
            act = Action.HIT
            self.actions.append(act)
            return act
        #print("I shouldn't make it here post splitting")
        tree.currentNode = tree.rootNode #if everythings been expanded, choose using selection!
        act = self.selection()  
        self.actions.append(act)
        
        ###Continue looking downward if available###
        tree.isTraversing = True
        temp = self.actions[0]
        while (not self.myTree.currentNode.isLeaf):
            temp = self.selection()
            self.actions.append(temp)
            if temp is (Action.STAND or Action.DOUBLE_DOWN):
                break
        #print(self.actions)
        return self.actions[0]
        
    def reset(self):
        self.actions = []
        self.myTree.inSplit = False
        self.myTree.isTraversing = False
        if self.myTree.currentNode.isLeaf:#if we are not on root or hit node go up
            self.myTree.currentNode = self.myTree.currentNode.parent
        
    def selection(self):
        c = 2
        #print("Entering Selection")
        current = self.myTree.currentNode
        hit = current.hitNode
        stand = current.standNode
        dd = current.ddNode
        split = None
        if self.myTree.hasSplitNode:
            split = self.myTree.rootNode.splitNode
        #print(stand.timesVisited)
        #print(hit.timesVisited) 
        #print(dd.timesVisited)
        N = hit.timesVisited+stand.timesVisited+dd.timesVisited
        #print(N)
        splitUCB = -1000
        if self.myTree.hasSplitNode:
            N = N + split.timesVisited
            splitUCB = (sum(split.values)/split.timesVisited)+c*math.sqrt((math.log(N)/split.timesVisited))
        #print(c * math.sqrt((math.log(N)/hit.timesVisited)))
        hitUCB =(sum(hit.values)/hit.timesVisited)+c*math.sqrt((math.log(N)/hit.timesVisited))
        standUCB = ((sum(stand.values)/stand.timesVisited)+c*math.sqrt((math.log(N)/stand.timesVisited)))
        ddUCB = ((sum(dd.values)/dd.timesVisited)+c*math.sqrt((math.log(N)/dd.timesVisited)))
        #print(hitUCB,standUCB,ddUCB,splitUCB)
        max = hitUCB
        if standUCB > hitUCB:
            max = standUCB
        if ddUCB > (standUCB and hitUCB):
            max = ddUCB
        if splitUCB > (standUCB and hitUCB and ddUCB and self.myTree.isTraversing == False):
            max = splitUCB
        if max is hitUCB:
            #print("in Hit")
            hit.timesVisited = hit.timesVisited + 1
            self.myTree.currentNode = self.myTree.currentNode.hitNode
            return Action.HIT
        if max is standUCB:  
            
            #print("in Stand")
            stand.timesVisited = stand.timesVisited + 1
            self.myTree.currentNode = self.myTree.currentNode.standNode
            return Action.STAND
        if max is ddUCB:
            
            #print("in dd")
            dd.timesVisited = dd.timesVisited + 1
            self.myTree.currentNode = self.myTree.currentNode.ddNode
            return Action.DOUBLE_DOWN
        if max is splitUCB: #dont go here if were not at root
            
            #print("in Split")
            split.timesVisited = split.timesVisited + 1
            self.myTree.currentNode = split
            self.myTree.inSplit = True
            return Action.SPLIT

class ConsolePlayer(Player):
    def get_action(self, cards, actions, dealer_cards):
        print()
        print("  Your cards:", format(cards), "(%.1f points)"%get_value(cards))
        print("  Dealer's visible card:", format(dealer_cards), "(%.1f points)"%get_value(dealer_cards))
        while True:
            print("  Which action do you want to take?")
            for i, a in enumerate(actions):
                print(" ", i+1, a.name)
            x = input()
            try:
                x = int(x)
                return actions[x-1]
            except Exception:
                print(" >>> Please enter a valid action number <<<")
    def reset(self):
        pass
        
class Dealer(Player):
    """
    The dealer has a fixed strategy: Hit when he has fewer than 17 points, otherwise stand.
    """
    def __init__(self):
        self.name = "Dealer"
    def get_action(self, cards, actions, dealer_cards):
        if get_value(cards) < 17:
            return Action.HIT
        return Action.STAND
        
def same_rank(a, b):
    return a.rank == b.rank
    
def same_value(a, b):
    return a.value == b.value

class Game:
    def __init__(self, cards, player, split_rule=same_value, verbose=True):
        self.cards = cards 
        self.player = player
        self.dealer = Dealer()
        self.dealer_cards = []
        self.player_cards = []
        self.split_cards = []
        self.verbose = verbose
        self.split_rule = split_rule

    def round(self):
        """
        Play one round of black jack. First, the player is asked to take actions until they
        either stand or have more than 21 points. The return value of this function is the 
        amount of money the player won.
        """
        self.deck = self.cards[:]
        random.shuffle(self.deck)
        self.dealer_cards = []
        self.player_cards = []
        self.bet = 2
        self.player.reset()
        self.dealer.reset()
        for i in range(2):
            self.deal(self.player_cards, self.player.name)
            self.deal(self.dealer_cards, self.dealer.name, i < 1)
        return self.play_round()
        
        
    def continue_round(self, player_cards, dealer_cards, bet):
        """
        Like round, but allows passing an initial game state in order to finish a partially played game.
       
        player_cards are the cards the player has in their hand
        dealer_cards are the visible cards (typically 1) of the dealer 
        bet is the current bet of the player 
        
        Note: For best results create a *new* Game object with a deck that has player_cards and dealer_cards removed.
        """
        self.deck = self.cards[:]
        random.shuffle(self.deck)
        self.bet = bet
        self.player_cards = player_cards[:] 
        self.dealer_cards = dealer_cards[:]
        while len(self.dealer_cards) < 2:
            self.deal(self.dealer_cards, self.dealer.name)
        return self.play_round()
        
    def play_round(self):
        """
        Function used to actually play a round of blackjack after the initial setup done in round or continue_round.
        
        Will first let the player take their actions and then proceed with the dealer.
        """
        cards = self.play(self.player, self.player_cards)
        if self.verbose:
            print("Dealer reveals: ", format(self.dealer_cards[-1]))
            print("Dealer has:", format(self.dealer_cards), "(%.1f points)"%get_value(self.dealer_cards))
        self.play(self.dealer, self.dealer_cards)
        reward = sum(self.reward(c) for c in cards)
        if self.verbose:
            print("Bet:", self.bet, "won:", reward, "\n")
        return reward

    def deal(self, cards, name, public=True):
        """
        Deal the next card to the given hand
        """
        card = self.deck[0]
        if self.verbose and public: 
            print(name, "draws", format(card))
        self.deck = self.deck[1:]
        cards.append(card)

    def play(self, player, cards, cansplit=True, postfix=""):
        """
        Play a round of blackjack for *one* participant (player or dealer).
        
        Note that a player may only split once, and only if the split_rule is satisfied (either two cards of the same rank, or of the same value)
        """
        while get_value(cards) < 21:
            actions = [Action.HIT, Action.STAND, Action.DOUBLE_DOWN]
            if len(cards) == 2 and cansplit and self.split_rule(cards[0], cards[1]):
                actions.append(Action.SPLIT)
            act = player.get_action(cards, actions, self.dealer_cards[:1])
            if act in actions:
                if self.verbose:
                    print(player.name, "does", act.name)
                if act == Action.STAND:
                    break
                if act == Action.HIT or act == Action.DOUBLE_DOWN:
                    self.deal(cards, player.name)
                if act == Action.DOUBLE_DOWN:
                    self.bet *= 2
                    break
                if act == Action.SPLIT:
                    pilea = cards[:1]
                    pileb = cards[1:]
                    if self.verbose:
                        print(player.name, "now has 2 hands")
                        print("Hand 1:", format(pilea))
                        print("Hand 2:", format(pileb))
                    self.play(player, pilea, False, " (hand 1)")
                    self.play(player, pileb, False, " (hand 2)")
                    return [pilea, pileb]
        if self.verbose:
            print(player.name, "ends with%s"%(postfix), format(cards), "with value", get_value(cards), "\n")
        return [cards]

    def reward(self, player_cards):
        """
        Calculate amount of money won by the player. Blackjack pays 3:2.
        """
        pscore = get_value(player_cards)
        dscore = get_value(self.dealer_cards)
        if self.verbose:
            print(self.player.name + ":", format(player_cards), "(%.1f points)"%(pscore))
            print(self.dealer.name + ":", format(self.dealer_cards), "(%.1f points)"%(dscore))
        
        if pscore > 21:
            return -self.bet
        result = -self.bet
        if pscore > dscore or dscore > 21:
            if pscore == 21 and len(self.player_cards) == 2:
                result = 3*self.bet/2
            result = self.bet
        if pscore == dscore and (pscore != 21 or len(self.player_cards) != 2):
            result = 0
        return result
        
        
player_types = {"default": Player, "timid": TimidPlayer, "basic": BasicStrategyPlayer, "mcts": MCTSPlayer, "console": ConsolePlayer}

# Our implementation allows us to define different deck "types", such as only even cards, 
# or even use made-up card values like "1.5"

deck_types = {"default": generate_deck(), 
              "high": generate_deck(ranks=[("2", 2), ("10", 10), ("Ace", 11), ("Fool", 12)]),
              "low": generate_deck(ranks=[("1.5", 1.5), ("2", 2),("2.2", 2.2), ("3", 3), ("3", 4), ("Ace", 11)], suits=["Hearts", "Spades", "Clubs", "Diamonds", "Swords", "Wands", "Bows"]),
              "even": generate_deck(ranks=[("2",2), ("4",4), ("6",6), ("8",8), ("10",10), ("Jack",10), ("Queen",10), ("King",10)]),
              "odd": generate_deck(ranks=[("3",3), ("5",5), ("7",7), ("9",9), ("Ace",11)]),
              "red": generate_deck(suits=["Diamonds", "Hearts"]),
              "random": generate_deck(ranks=random.sample([("2",2), ("3",3), ("4",4), ("5",5), ("6",6), ("7",7), ("8",8), ("9",9), ("10",10), ("Jack",10), ("Queen",10), ("King",10), ("Ace",11)], random.randint(5,13)))}

def main(ptype="default", dtype="default", n=100, split_rule=same_value, verbose=True): #default n is 100
    deck = deck_types[dtype]


    g = Game(deck, player_types[ptype]("Sir Gladington III, Esq.", deck[:]), split_rule, verbose)
    points = []
    for i in range(n):
        points.append(g.round())
    print("Average points: ", sum(points)*1.0/n)
    

# run `python blackjack.py --help` for usage information
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a simulation of a Blackjack agent.')
    parser.add_argument('player', nargs="?", default="default", 
                        help='the player type (available values: %s)'%(", ".join(player_types.keys())))
    parser.add_argument('-n', '--count', dest='count', action='store', default=100,
                        help='How many games to run')
    parser.add_argument('-s', '-q', '--silent', '--quiet', dest='verbose', action='store_const', default=True, const=False,
                        help='Do not print game output (only average score at the end is printed)')
    parser.add_argument('-r', '--rank', '--rank-split', dest='split', action='store_const', default=same_value, const=same_rank,
                        help="Only allow split when the player's cards have the same rank (default: allow split when they have the same value)")
    parser.add_argument('-d', "--deck", metavar='D', dest="deck", nargs=1, default=["default"], 
                        help='the deck type to use (available values: %s)'%(", ".join(deck_types.keys())))
    args = parser.parse_args()
    if args.player not in player_types:
        print("Invalid player type: %s. Available options are: \n%s"%(args.player, ", ".join(player_types.keys())))
        sys.exit(-1)
    if args.deck[0] not in deck_types:
        print("Invalid deck type: %s. Available options are: \n%s"%(args.deck, ", ".join(deck_types.keys())))
        sys.exit(-1)
    main(args.player, args.deck[0], int(args.count), args.split, args.verbose)