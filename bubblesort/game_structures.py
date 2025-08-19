point_per_kill = 10
point_per_assist = 5
point_per_100_damage = 2
point_loss_per_death = 5

class Kill:
    def __init__(self, player, target):
        self.player = player
        self.target = target

    def execute(self):
        print(f"{self.player.nickname} scored a kill on {self.target.nickname}!")


class Assist:
    def __init__(self, player, target):
        self.player = player
        self.target = target

    def execute(self):
        print(f"{self.player.nickname} assisted in killing {self.target.nickname}!")


class Death:
    def __init__(self, player, killer):
        self.player = player
        self.killer = killer

    def execute(self):
        print(f"{self.player.nickname} has died!")


class Player:
    def __init__(self, nickname, points, level):
        self.nickname = nickname      
        self.points = points   
        self.level = level

    def describe(self):
        print(f"Nickname: {self.nickname}, Points: {self.points}, Level: {self.level}")
        
    def remove_points(self, remove_points):
        if (self.points - remove_points < 0):
            self.level -= 1
            self.points = max(0, 100 - remove_points)   
        else:
            self.points -= remove_points
        print(f"{self.nickname} has lost {remove_points} points! Total points: {self.points}")
            
    def add_points(self, points):
        if self.points + points >= 100:
            self.level += (self.points + points) // 100
            self.points = (self.points + points) % 100
        else:
            self.points += points
        print(f"{self.nickname} has gained {points} points! Total points: {self.points}")


class MatchStats:
    def __init__(self, player):
        self.player = player
        self.kills = []
        self.assists = []
        self.deaths = []
        self.damage = 0

    def increment_kills(self, target):
        self.kills.append(Kill(self.player, target))

    def increment_assists(self, target):
        self.assists.append(Assist(self.player, target))
    
    def increment_deaths(self, killer):
        self.deaths.append(Death(self.player, killer))

    def increment_damage(self, damage):
        self.damage += damage
        print(f"{self.player.nickname} has dealt {damage} damage! Total damage: {self.damage}")
        
    def display_stats(self):
        self.player.describe()
        print(f"Kills: {len(self.kills)}, Assists: {len(self.assists)}, Deaths: {len(self.deaths)}, Damage: {self.damage}")


class Match:
    def __init__(self, players, PlayersMatchStats):
        self.players = players
        self.PlayersMatchStats = PlayersMatchStats

    def startMatch(self):
        print("Match started! Players are ready:")
        for player in self.players:
            player.describe()

    def finishMatch(self):
        print("\n--- Match Finished! Calculating rewards... ---\n")

        result_map = {}
        
        for player in self.players:
            stats = self.PlayersMatchStats[player]
            
            points_from_damage = (stats.damage // 100) * point_per_100_damage
            points_from_kills = 0
            points_from_assists = 0

            for kill in stats.kills:
                points_from_kills += point_per_kill * (1 + (kill.target.level / player.level))

            for assist in stats.assists:
                points_from_assists += point_per_assist * (1 + (assist.target.level / player.level))

            total_points = points_from_kills + points_from_assists + points_from_damage

            for death in stats.deaths:
                total_points -= point_loss_per_death * (1 + (death.killer.level / player.level))

            if total_points < 0:
                player.remove_points(abs(total_points))
            else:
                player.add_points(total_points)

            print(f"{player.nickname} => "
                  f"Kills: {len(stats.kills)}, Assists: {len(stats.assists)}, "
                  f"Deaths: {len(stats.deaths)}, Damage: {stats.damage}, "
                  f"Total Earned: {total_points}\n")
            
            result_map[player] = {
                "points_earned": total_points,
                "kills": len(stats.kills),
                "assists": len(stats.assists),
                "deaths": len(stats.deaths),
                "damage": stats.damage
            }

        print("\n--- End of Match ---")
        return result_map
