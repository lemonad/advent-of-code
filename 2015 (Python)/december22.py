"""
December 22, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from itertools import combinations
from common.puzzlesolver import PuzzleSolver


class Solver(PuzzleSolver):

    LARGE_SPENT = 1000000

    # If duration = 0 then actions are immediate.
    spells = {}
    spells['Magic Missile'] = {'Cost': 53, 'Damage': 4}
    spells['Drain'] = {'Cost': 73, 'Damage': 2, 'Heal': 2}
    spells['Shield'] = {'Cost': 113, 'Armor': 7, 'Duration': 6}
    spells['Poison'] = {'Cost': 173, 'DamagePerTurn': 3, 'Duration': 6}
    spells['Recharge'] = {'Cost': 229, 'ManaPerTurn': 101, 'Duration': 5}

    def __init__(self, *args, **kwargs):
        if 'level' in kwargs:
            Solver.level = kwargs['level']
            del kwargs['level']
        else:
            self.level = 'easy'
        super(Solver, self).__init__(*args, **kwargs)
        self.max_spent = self.LARGE_SPENT

    def does_player_win_fight(
            self, hit_points, armor, boss_hit_points, boss_damage,
            mana, spent_mana=0, players_turn=True, active_spells={}):
        # print(self.level, mana, spent_mana, hit_points, boss_hit_points,
        #       "player" if players_turn else "boss")
        if spent_mana >= self.max_spent:
            # print("Exit early (max_spent = %d)" % self.max_spent)
            return spent_mana

        if players_turn and self.level == 'hard':
            hit_points -= 1
            if hit_points <= 0:
                # print("Player loses (out of HP)")
                return Solver.LARGE_SPENT

        for name, time_left in active_spells.items():
            spell = Solver.spells[name]
            if time_left > 0:
                if 'DamagePerTurn' in spell:
                    boss_hit_points -= spell['DamagePerTurn']
                if 'ManaPerTurn' in spell:
                    mana += spell['ManaPerTurn']
                if 'Armor' in spell and time_left == 1:
                    armor -= spell['Armor']
                active_spells[name] -= 1

        if boss_hit_points <= 0:
            # print("Player wins!!!")
            if spent_mana < self.max_spent:
                self.max_spent = spent_mana
            return spent_mana

        if players_turn:
            min_spent = Solver.LARGE_SPENT
            # Cast new spell.
            spell_cast = False
            for name, effect in Solver.spells.items():
                spell = Solver.spells[name]

                if name in active_spells and active_spells[name] > 0:
                    continue
                if spell['Cost'] > mana:
                    continue

                spell_cast = True

                new_mana = mana - spell['Cost']
                new_spent_mana = spent_mana + spell['Cost']

                new_armor = armor
                if 'Armor' in spell:
                    new_armor += spell['Armor']

                new_boss_hit_points = boss_hit_points
                if 'Damage' in spell:
                    new_boss_hit_points -= spell['Damage']

                new_hit_points = hit_points
                if 'Heal' in spell:
                    new_hit_points += spell['Heal']

                new_active_spells = active_spells.copy()
                if ('Duration' in spell and spell['Duration'] > 0):
                    new_active_spells[name] = spell['Duration']

                spent = self.does_player_win_fight(
                        new_hit_points, new_armor, new_boss_hit_points,
                        boss_damage, new_mana, new_spent_mana,
                        not players_turn, new_active_spells)
                if spent < min_spent:
                    min_spent = spent
            # Player can't afford spell and loses.
            if not spell_cast:
                # print("Player loses (can't afford any spell)")
                return Solver.LARGE_SPENT
        else:
            hit_points -= max(1, boss_damage - armor)
            if hit_points <= 0:
                # print("Player loses (out of HP)")
                return Solver.LARGE_SPENT

            min_spent = self.does_player_win_fight(
                    hit_points, armor, boss_hit_points, boss_damage,
                    mana, spent_mana, not players_turn, active_spells)
        return min_spent

    def solve(self):
        """Solution for part one or part two."""
        boss_stats = self.as_dict()
        for key, val in boss_stats.items():
            boss_stats[key] = int(val)

        return self.does_player_win_fight(
                50, 0,
                boss_stats['Hit Points'],
                boss_stats['Damage'],
                500)

if __name__ == '__main__':
    s = Solver(from_file='input/dec22.in')
    one = s.solve()
    print("Least amount of mana spent and fight still won? %d" % one)

    # Solver is relying on class attributes during recursion so
    # we need to instantiate new solver.
    s = Solver(from_file='input/dec22.in', level='hard')
    two = s.solve()
    print("Least amount of mana spent and fight still won (hard)? %d" % two)

    assert(one == 953)
    assert(two == 1289)
