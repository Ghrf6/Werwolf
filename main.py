import random

class Player:
    def __init__(self, role):
        self.role = role
        self.alive = True
        self.healed = False
        self.in_love = False
        self.targeted_by_secretary = False
        self.is_known_werewolf = False

class WerewolfGame:
    def __init__(self, num_werewolves, num_villagers, witch_present, hunter_present, amor_present, blinking_girl_present, secretary_present, seer_present):
        self.players = []
        self.witch = None
        self.hunter = None
        self.amor = None
        self.blinking_girl = None
        self.secretary = None
        self.seer = None
        self.heal_potion_used = False
        self.kill_potion_used = False
        self.lovers = []
        self.init_players(num_werewolves, num_villagers, witch_present, hunter_present, amor_present, blinking_girl_present, secretary_present, seer_present)
    
    def init_players(self, num_werewolves, num_villagers, witch_present, hunter_present, amor_present, blinking_girl_present, secretary_present, seer_present):
        self.players = []
        for _ in range(num_werewolves):
            self.players.append(Player('Werewolf'))
        for _ in range(num_villagers):
            self.players.append(Player('Villager'))
        if witch_present:
            self.witch = Player('Witch')
            self.players.append(self.witch)
        if hunter_present:
            self.hunter = Player('Hunter')
            self.players.append(self.hunter)
        if amor_present:
            self.amor = Player('Amor')
            self.players.append(self.amor)
        if blinking_girl_present:
            self.blinking_girl = Player('BlinkingGirl')
            self.players.append(self.blinking_girl)
        if secretary_present:
            self.secretary = Player('Secretary')
            self.players.append(self.secretary)
        if seer_present:
            self.seer = Player('Seer')
            self.players.append(self.seer)
        random.shuffle(self.players)
        self.choose_lovers()
    
    def choose_lovers(self):
        if self.amor:
            possible_lovers = [player for player in self.players if player != self.amor]
            self.lovers = random.sample(possible_lovers, 2)
            for lover in self.lovers:
                lover.in_love = True
    
    def secretary_target(self):
        if self.secretary and self.secretary.alive:
            possible_targets = [player for player in self.players if player != self.secretary and player.alive]
            if possible_targets:
                target = random.choice(possible_targets)
                target.targeted_by_secretary = True
                return target
        return None

    def seer_vision(self):
        if self.seer and self.seer.alive:
            possible_targets = [player for player in self.players if player != self.seer and player.alive and not player.is_known_werewolf]
            if possible_targets:
                target = random.choice(possible_targets)
                if target.role == 'Werewolf':
                    target.is_known_werewolf = True
    
    def night_phase(self):
        self.seer_vision()
        secretary_target = self.secretary_target()
        if self.blinking_girl and self.blinking_girl.alive and random.random() < 0.40:
            self.blinking_girl.alive = False
        else:
            non_werewolves = [player for player in self.players if player.role != 'Werewolf' and player.alive]
            if non_werewolves:
                victim = random.choice(non_werewolves)
                if self.witch and victim == self.witch and self.witch.alive:
                    if not self.heal_potion_used:
                        self.witch.alive = True
                        self.heal_potion_used = True
                    else:
                        self.witch.alive = False
                        self.use_kill_potion()
                elif self.witch and self.witch.alive and not self.heal_potion_used and random.random() < 0.25:
                    self.witch.healed = True
                    victim.healed = True
                    self.heal_potion_used = True
                else:
                    if victim == secretary_target:
                        self.secretary.alive = False
                        victim.alive = False
                    elif self.secretary and victim.role == 'Werewolf' and self.secretary.alive and victim == secretary_target:
                        self.secretary.alive = False
                    else:
                        if victim in self.lovers and any(lover.role == 'Werewolf' for lover in self.lovers):
                            if len(non_werewolves) == 1:
                                victim.alive = False
                            else:
                                return
                        else:
                            victim.alive = False
                            if self.hunter and victim == self.hunter and self.hunter.alive:
                                self.hunter_shoots()
                            if self.witch and self.witch.alive and not self.kill_potion_used:
                                self.use_kill_potion()
    
    def use_kill_potion(self):
        if not self.kill_potion_used:
            if random.random() < 0.75:
                werewolf_victims = [player for player in self.players if player.role == 'Werewolf' and player.alive]
                if werewolf_victims:
                    killed_werewolf = random.choice(werewolf_victims)
                    killed_werewolf.alive = False
            else:
                innocent_victims = [player for player in self.players if player.role != 'Werewolf' and player.alive]
                if innocent_victims:
                    killed_innocent = random.choice(innocent_victims)
                    killed_innocent.alive = False
            self.kill_potion_used = True
    
    def hunter_shoots(self):
        if random.random() < 0.60:
            werewolf_victims = [player for player in self.players if player.role == 'Werewolf' and player.alive]
            if werewolf_victims:
                killed_werewolf = random.choice(werewolf_victims)
                killed_werewolf.alive = False
        else:
            innocent_victims = [player for player in self.players if player.role != 'Werewolf' and player.alive]
            if innocent_victims:
                killed_innocent = random.choice(innocent_victims)
                killed_innocent.alive = False
    
    def day_phase(self):
        alive_players = [player for player in self.players if player.alive]
        innocent = [player for player in alive_players if player.role != 'Werewolf']
        werewolves = [player for player in alive_players if player.role == 'Werewolf']
        known_werewolves = [player for player in alive_players if player.is_known_werewolf]

        if innocent and werewolves:
            accused = []
            if self.blinking_girl and self.blinking_girl.alive:
                accused.append(random.choice(innocent))
                accused.append(random.choice(werewolves))
                accused.append(random.choice(alive_players))
            else:
                if random.random() < 0.55 and werewolves:
                    accused.append(random.choice(werewolves))
                accused.append(random.choice(alive_players))
                if random.random() < 0.5 and werewolves:
                    accused.append(random.choice(werewolves))
                else:
                    accused.append(random.choice(innocent))
            
            if known_werewolves:
                accused.append(random.choice(known_werewolves))

            votes = {self.players.index(player): 0 for player in alive_players}
            for player in alive_players:
                if player.role == 'Werewolf':
                    votes[self.players.index(random.choice(innocent))] += 1
                else:
                    if player in self.lovers:
                        non_lover_accused = [s for s in accused if s not in self.lovers]
                        if non_lover_accused:
                            votes[self.players.index(random.choice(non_lover_accused))] += 1
                        else:
                            votes[self.players.index(random.choice(accused))] += 1
                    elif player == self.seer:
                        non_innocent_accused = [s for s in accused if s.role != 'Villager']
                        if non_innocent_accused:
                            votes[self.players.index(random.choice(non_innocent_accused))] += 1
                        else:
                            votes[self.players.index(random.choice(accused))] += 1
                    else:
                        votes[self.players.index(random.choice(accused))] += 1

            accused_index = max(votes, key=votes.get)
            self.players[accused_index].alive = False

    def game_status(self):
        alive_werewolves = [player for player in self.players if player.role == 'Werewolf' and player.alive]
        alive_villagers = [player for player in self.players if player.role != 'Werewolf' and player.alive]
        lovers_alive = self.lovers_alive()
        
        if not alive_werewolves:
            if lovers_alive:
                return "Villagers and Lovers"
            return "Villagers"
        if not alive_villagers:
            if lovers_alive:
                return "Werewolves and Lovers"
            return "Werewolves"
        return None
    
    def lovers_alive(self):
        return all(lover.alive for lover in self.lovers)

    def simulate_game(self):
        while True:
            self.night_phase()
            winner = self.game_status()
            if winner:
                return winner
            self.day_phase()
            winner = self.game_status()
            if winner:
                return winner

# Define the number of werewolves, villagers, and the number of simulations
num_werewolves = 3
num_villagers = 0
witch_present = True
hunter_present = True
amor_present = True
blinking_girl_present = True
secretary_present = True
seer_present = True
num_simulations = 10000

# Initialize the variables for the wins
wolf_wins = 0
village_wins = 0

# Run the simulations
for _ in range(num_simulations):
    game = WerewolfGame(num_werewolves, num_villagers, witch_present, hunter_present, amor_present, blinking_girl_present, secretary_present, seer_present)
    winner = game.simulate_game()
    if winner == "Werewolves":
        wolf_wins += 1
    elif winner == "Villagers":
        village_wins += 1
    elif winner == "Werewolves and Lovers":
        wolf_wins += 1
    elif winner == "Villagers and Lovers":
        village_wins += 1

# Print the results
print(f"Werewolves won {wolf_wins} times.")
print(f"Villagers won {village_wins} times.")
