'''
Concepts Covered: Object interaction, inheritance, random module usage
Task:
Create a Character class with attributes like name, health, and attack_power.
Add methods for attacking another character and taking damage.
Implement subclasses such as Warrior, Mage, and Archer with unique abilities.
Challenge Extension: Add an inventory system where characters can pick up and use items.
'''
import random
global combatturn
combatturn = 0
def startcombat(player1, player2):
    global combatturn
    combatturn = 0 # reset combat turn
    while not player1.charisdead and not player2.charisdead:
        if combatturn % 2 == 0:
            print(f'{player1.name}, it is your turn. \nYour health: {player1.currenthealth}/{player1.maxhealth}\nEnemy health: {player2.currenthealth}/{player2.maxhealth}\nActions: ')
            for n in range(len(player1.charactions)):
                print(f'{n+1}) {player1.charactions[n]}') # Base example: '1) Attack 2) Flee'
            while True:
                p1action = input(f'{player1.name}, input your action: ').upper()
                if p1action in player1.charactions:
                    if p1action == 'ATTACK':
                        player1.attack(player2)
                        break
                    if p1action == 'FLEE':
                        print(f'{player1.name} is trying to flee...')
                        if random.randint(0, player1.fleevar) == 0:
                            print(f'{player1.name} has fled!')
                            combatturn = -1 # end combat
                            break
                        else:
                            print(f'{player1.name} has failed to flee!')
                            break
                else: print(f'{player1.name}, that is an invalid action.')
            if combatturn == -1:
                print(f'Combat is over.')
                break
            else:
                combatturn = combatturn + 1
                print(f'Combat Turn: {combatturn}')
    print(f'Combat is over.')
    if player1.charisdead: print(f'{player2.name} has won!')
    if player2.charisdead: print(f'{player1.name} has won!')

class Character:
    fleevar = 6
    charactions = ['ATTACK', 'FLEE']
    def __init__(self, name="John", maxhealth=1, attackpower=1):
        self.charisdead = False
        self.currenthealth = maxhealth
        self.name, self.maxhealth, self.attackpower = name, maxhealth, attackpower
    
    def __repr__(self):
        return f'Name: {self.name}, Health:{self.currenthealth}/{self.maxhealth}, Attack Power:{self.attackpower}, Is Dead:{self.charisdead}, Actions: {self.charactions}'
    
    def attack(self, other, modifier=0):
        other.currenthealth = other.currenthealth - (self.attackpower + modifier)
        print(f'{self.name} has attacked {other.name} for {self.attackpower + modifier} damage!')
        print(f'{other.name} has {other.currenthealth} health left.')
        if other.currenthealth <= 0:
            other.currenthealth = 0
            other.charisdead = True

c1 = Character('Albert', 10, 2)
c2 = Character('Mark', 20)

print(c1)
print(c2)

startcombat(c1, c2)