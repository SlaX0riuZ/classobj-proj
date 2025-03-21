import math
import random

# ----------------------------- [base variables]

global combatturn
def printline():
    print('-------------------------------------')
combatturn = 0

# ----------------------------- [all-encompassing combat function]

def startcombat(player1, player2):
    def taketurn(current, opponent):
        print(f'{current.name}, it is your turn. \nYour health: {current.currenthealth}/{current.maxhealth}\nEnemy health: {opponent.currenthealth}/{opponent.maxhealth}\nActions: ')
        for n in range(len(current.charactions)):
            print(f'{n+1}) {current.charactions[n]}') # Base example: '1) Attack 2) Flee'
        while True:
            currentplayeraction = input(f'{current.name}, input your action: ').upper()
            if currentplayeraction in current.charactions:
                if currentplayeraction == 'ATTACK': current.attack(opponent)
                elif currentplayeraction == 'FLEE': current.flee()
                elif currentplayeraction == 'DISTRACT': current.distract(opponent)
                elif currentplayeraction == 'HEAL': current.heal()
                elif currentplayeraction == 'EMPOWER': current.empower(opponent)
                break
            else: print(f'{current.name}, that is an invalid action.')
    global combatturn
    combatturn = 0 # reset combat turn
    while not player1.charisdead and not player2.charisdead:
        if combatturn == -1: break # exit combat on successful flee
        else:
            printline()
            combatturn = combatturn + 1
            print(f'Combat Turn: {combatturn}')
            printline()
            if combatturn % 2 == 0: taketurn(player1, player2)
            elif combatturn % 2 != 0: taketurn(player2, player1)
    printline()
    print(f'Combat is over.')
    printline()
    if player1.charisdead: print(f'{player2.name} has won!')
    if player2.charisdead: print(f'{player1.name} has won!')

# ----------------------------- [base character class and methods]

class Character:
    fleevar = 6
    charactions = ['ATTACK', 'FLEE']
    maxhealth = 25
    attackpower = 2
    critchance = 8
    def __init__(self, name="John", maxhealth=25, attackpower=2, critchance=8):
        self.charisdead, self.currenthealth, self.critchance = False, maxhealth, critchance
        self.name, self.maxhealth, self.attackpower = name, maxhealth, attackpower
    def __repr__(self):
        return f'Name: {self.name}, Health: {self.currenthealth}/{self.maxhealth}, \
Attack Power: {self.attackpower}, Is Dead: {self.charisdead}, Actions: {self.charactions}, Flee Chance: 1/{self.fleevar}'
    def attack(self, other, modifier=0):
        if random.randint(0, self.critchance) == 0: # based on fleevar to benefit rogue
            print('Critical Hit!')
            modifier = self.attackpower # double damage
        other.currenthealth = other.currenthealth - (self.attackpower + modifier)
        print(f'{self.name} has attacked {other.name} for {self.attackpower + modifier} damage!')
        print(f'{other.name} has {other.currenthealth} health left.')
        if other.currenthealth <= 0: other.currenthealth, other.charisdead = 0, True
    def flee(self):
        print(f'{self.name} is trying to flee...')
        if random.randint(0, self.fleevar) == 0:
            print(f'{self.name} has fled!')
            global combatturn
            combatturn = -1 # end combat
        else: print(f'{self.name} has failed to flee!')

# ----------------------------- [subclass creation]

class Rogue(Character):
    def __init__(self, name="Rogue", maxhealth=25, attackpower=2, critchance=8):
        super().__init__(name, maxhealth, attackpower, critchance)
        self.maxhealth = math.ceil(maxhealth * 0.75) # set base health to 3/4 normal
        self.currenthealth, self.fleevar, self.name = self.maxhealth, 4, name
        self.charactions = ['ATTACK', 'FLEE', 'DISTRACT'] # special action: distract
    def distract(self, other):
        print(f'{self.name} is trying to distract {other.name}...')
        if random.randint(0, 3) == 0 and self.fleevar > 2: # 1/3 success rate
            print(f'{self.name} has distracted {other.name}!')
            print(f'{self.name}\'s evasion has increased!') # increase fleevar if successful
            self.fleevar = self.fleevar - 1
        else: print(f'{self.name} has failed to distract {other.name}.')

class Wizard(Character):
    def __init__(self, name="Wizard", maxhealth=25, attackpower=3, critchance=8):
        super().__init__(name, maxhealth, attackpower, critchance)
        self.maxhealth = math.ceil(self.maxhealth * 0.5) # halve base health to balance
        self.currenthealth, self.name = self.maxhealth, name # no need to change fleevar from default
        self.charactions = ['ATTACK', 'FLEE', 'HEAL'] # special action: healing
    def heal(self):
        healamount = random.randint(0, math.ceil((self.maxhealth/2))) # max heals = 1/2 max health
        if self.currenthealth + healamount > self.maxhealth: healamount = self.maxhealth - self.currenthealth # override heal value so it doesn't overheal
        print(f'{self.name} has healed {healamount} health!')
        self.currenthealth = self.currenthealth + healamount # actual healing

class Fighter(Character):
    def __init__(self, name="Fighter", maxhealth=25, attackpower=3, critchance=6):
        super().__init__(name, maxhealth, attackpower, critchance)
        self.currenthealth, self.name = self.maxhealth, name
        self.charactions = ['ATTACK', 'FLEE', 'EMPOWER'] # special action: empower
        self.empoweruses = 0 # variable to counter empower stacking
    def empower(self, other):
        print(f'{self.name} is trying to empower themselves...')
        if random.randint(0, 5+self.empoweruses) <= 3: # 2/3 success first try, scales with use amount
            print(f'{other.name} has brought upon {self.name}\'s wrath!')
            print(f'{self.name}\'s damage has increased!')
            self.attackpower = self.attackpower + 1
        else: print(f'{self.name} lost their concentration.')

# ----------------------------- [character creation and combat initiation]

c1 = Fighter('Albert')
c2 = Rogue('Mark')

print(c1)
print(c2)

startcombat(c1, c2)