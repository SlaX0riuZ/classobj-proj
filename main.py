'''
Concepts Covered: Object interaction, inheritance, random module usage
Task:
Create a Character class with attributes like name, health, and attack_power.
Add methods for attacking another character and taking damage.
Implement subclasses such as Warrior, Mage, and Archer with unique abilities.
Challenge Extension: Add an inventory system where characters can pick up and use items.
'''
import math
import random
global combatturn
def printline():
    print('-------------------------------------')
combatturn = 0
def startcombat(player1, player2):
    def taketurn(current, opponent):
        print(f'{current.name}, it is your turn. \nYour health: {current.currenthealth}/{current.maxhealth}\nEnemy health: {opponent.currenthealth}/{opponent.maxhealth}\nActions: ')
        for n in range(len(current.charactions)):
            print(f'{n+1}) {current.charactions[n]}') # Base example: '1) Attack 2) Flee'
        while True:
            p1action = input(f'{current.name}, input your action: ').upper()
            if p1action in current.charactions:
                if p1action == 'ATTACK':
                    current.attack(opponent)
                    break
                if p1action == 'FLEE':
                    print(f'{current.name} is trying to flee...')
                    if random.randint(0, current.fleevar) == 0:
                        print(f'{current.name} has fled!')
                        combatturn = -1 # end combat
                        break
                    else:
                        print(f'{current.name} has failed to flee!')
                        break
                if p1action == 'DISTRACT':
                    player1.distract(opponent)
                    break
                if p1action == 'HEAL':
                    player1.heal()
                    break
            else: print(f'{current.name}, that is an invalid action.')
    global combatturn
    combatturn = 0 # reset combat turn
    while not player1.charisdead and not player2.charisdead:
        if combatturn == -1:
            break # exit combat on successful flee
        else:
            printline()
            combatturn = combatturn + 1
            print(f'Combat Turn: {combatturn}')
            printline()
            if combatturn % 2 == 0:
                taketurn(player1, player2)
            elif combatturn % 2 != 0:
                taketurn(player2, player1)
    printline()
    print(f'Combat is over.')
    printline()
    if player1.charisdead: print(f'{player2.name} has won!')
    if player2.charisdead: print(f'{player1.name} has won!')

class Character:
    fleevar = 6
    charactions = ['ATTACK', 'FLEE']
    maxhealth = 10
    attackpower = 2
    def __init__(self, name="John", maxhealth=20, attackpower=2):
        self.charisdead = False
        self.currenthealth = maxhealth
        self.name, self.maxhealth, self.attackpower = name, maxhealth, attackpower
    
    def __repr__(self):
        return f'Name: {self.name}, Health: {self.currenthealth}/{self.maxhealth}, Attack Power: {self.attackpower}, Is Dead: {self.charisdead}, Actions: {self.charactions}, Flee Chance: 1/{self.fleevar}'
    
    def attack(self, other, modifier=0):
        if random.randint(0, 20) == 0:
            print('Critical Hit!')
            modifier = self.attackpower # double damage
        other.currenthealth = other.currenthealth - (self.attackpower + modifier)
        print(f'{self.name} has attacked {other.name} for {self.attackpower + modifier} damage!')
        print(f'{other.name} has {other.currenthealth} health left.')
        if other.currenthealth <= 0:
            other.currenthealth = 0
            other.charisdead = True

class Rogue(Character):
    Character.maxhealth = math.ceil(Character.maxhealth * 0.75) # set base health to 3/4
    Character.currenthealth = Character.maxhealth
    Character.fleevar = 4
    Character.charactions = ['ATTACK', 'FLEE', 'DISTRACT'] # special action: distraction
    def __init__(self, name="Rogue"):
        super().__init__(name, maxhealth=...)
        self.maxhealth, self.currenthealth, self.fleevar, self.charactions = Character.maxhealth, Character.currenthealth, Character.fleevar, Character.charactions
        self.name = name
    def distract(self, other):
        print(f'{self.name} is trying to distract {other.name}...')
        if random.randint(0, 3) == 0 and self.fleevar > 2: # 1/3 success rate
            print(f'{self.name} has distracted {other.name}!')
            print(f'{self.name}\'s evasion has increased!') # increase fleevar if successful
            self.fleevar = self.fleevar - 1
        else: print(f'{self.name} has failed to distract {other.name}.')

class Wizard(Character):
    Character.maxhealth = math.ceil(Character.maxhealth * 0.5) # halve base health to balance out
    Character.currenthealth = Character.maxhealth
    Character.fleevar = 6
    Character.charactions = ['ATTACK', 'FLEE', 'HEAL'] # special action: healing
    def heal(self):
        healamount = random.randint(0, math.ceil((self.maxhealth/2))) # max heals = 1/2 max health
        if self.currenthealth + healamount > self.maxhealth:
            healamount = self.maxhealth - self.currenthealth # override heal value so it doesn't overheal
        print(f'{self.name} has healed {healamount} health!')
        self.currenthealth = self.currenthealth + healamount # actual healing

c1 = Wizard('Albert')
c2 = Rogue('Mark')

print(c1)
print(c2)

startcombat(c1, c2)