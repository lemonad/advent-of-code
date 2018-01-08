"""
December 21, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from itertools import combinations
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    weapons = {}
    weapons['Dagger'] = {'Cost': 8, 'Damage': 4, 'Armor': 0}
    weapons['Shortsword'] = {'Cost': 10, 'Damage': 5, 'Armor': 0}
    weapons['Warhammer'] = {'Cost': 25, 'Damage': 6, 'Armor': 0}
    weapons['Longsword'] = {'Cost': 40, 'Damage': 7, 'Armor': 0}
    weapons['Greataxe'] = {'Cost': 74, 'Damage': 8, 'Armor': 0}

    armor = {}
    armor['None'] = {'Cost': 0, 'Damage': 0, 'Armor': 0}
    armor['Leather'] = {'Cost': 13, 'Damage': 0, 'Armor': 1}
    armor['Chainmail'] = {'Cost': 31, 'Damage': 0, 'Armor': 2}
    armor['Splintmail'] = {'Cost': 53, 'Damage': 0, 'Armor': 3}
    armor['Bandedmail'] = {'Cost': 75, 'Damage': 0, 'Armor': 4}
    armor['Platemail'] = {'Cost': 102, 'Damage': 0, 'Armor': 5}

    rings = {}
    rings['No damage ring'] = {'Cost': 0, 'Damage': 0, 'Armor': 0}
    rings['No defense ring'] = {'Cost': 0, 'Damage': 0, 'Armor': 0}
    rings['Damage +1'] = {'Cost': 25, 'Damage': 1, 'Armor': 0}
    rings['Damage +2'] = {'Cost': 50, 'Damage': 2, 'Armor': 0}
    rings['Damage +3'] = {'Cost': 100, 'Damage': 3, 'Armor': 0}
    rings['Defense +1'] = {'Cost': 20, 'Damage': 0, 'Armor': 1}
    rings['Defense +2'] = {'Cost': 40, 'Damage': 0, 'Armor': 2}
    rings['Defense +3'] = {'Cost': 80, 'Damage': 0, 'Armor': 3}

    def __init__(self, *args, **kwargs):
        super(Solver, self).__init__(*args, **kwargs)

    @staticmethod
    def does_player_win_fight(hit_points, damage, armor,
                              boss_hit_points, boss_damage, boss_armor):

        players_turn = True
        while True:
            if players_turn:
                boss_hit_points -= max(1, damage - boss_armor)
                if boss_hit_points <= 0:
                    return True
            else:
                hit_points -= max(1, boss_damage - armor)
                if hit_points <= 0:
                    return False
            players_turn = not players_turn

    def solve(self):
        """Solution for both parts."""
        boss_stats = self.as_dict()
        for key, val in boss_stats.items():
            boss_stats[key] = int(val)

        min_cost = 10000000
        max_cost = -1

        for w in self.weapons:
            for a in self.armor:
                for r1, r2 in combinations(self.rings.keys(), 2):
                    # print("Weapon: %s, Armor: %s, Rings: %s and %s" % (
                    #     w, a, r1, r2))

                    cost = (self.weapons[w]['Cost'] +
                            self.armor[a]['Cost'] +
                            self.rings[r1]['Cost'] +
                            self.rings[r2]['Cost'])
                    damage = (self.weapons[w]['Damage'] +
                              self.armor[a]['Damage'] +
                              self.rings[r1]['Damage'] +
                              self.rings[r2]['Damage'])
                    armor = (self.weapons[w]['Armor'] +
                             self.armor[a]['Armor'] +
                             self.rings[r1]['Armor'] +
                             self.rings[r2]['Armor'])

                    # Simulate
                    if Solver.does_player_win_fight(
                            100, damage, armor,
                            boss_stats['Hit Points'],
                            boss_stats['Damage'],
                            boss_stats['Armor']):
                        # print("Player wins! (cost %d)" % cost)
                        if min_cost > cost:
                            min_cost = cost
                    else:
                        # print("Boss wins! (cost %d)" % cost)
                        if max_cost < cost:
                            max_cost = cost

        return (min_cost, max_cost)


if __name__ == '__main__':
    s = Solver(from_file='input/dec21.in')
    (one, two) = s.solve()
    print("Least amount of gold spent and fight still won? %d" % one)
    print("Most amount of gold spent and fight still lost? %d" % two)

    assert(one == 121)
    assert(two == 201)
