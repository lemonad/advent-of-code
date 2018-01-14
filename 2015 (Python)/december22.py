"""
December 22, Advent of Code 2015 (Jonas Nockert / @lemonad)

"""
from common.puzzlesolver import PuzzleSolver


class PlayerState:
    def __init__(self, hp, mana, armor=0, spent_mana=0):
        self.hp = hp
        self.armor = armor
        self.mana = mana
        self.spent_mana = spent_mana

    def copy(self):
        return PlayerState(self.hp, self.mana, self.armor, self.spent_mana)


class BossState:
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def copy(self):
        return BossState(self.hp, self.damage)


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

    @classmethod
    def process_spell_effects(cls, player, boss, active_spells):
        for name, time_left in active_spells.items():
            if time_left > 0:
                spell = cls.spells[name]
                if 'DamagePerTurn' in spell:
                    boss.hp -= spell['DamagePerTurn']
                if 'ManaPerTurn' in spell:
                    player.mana += spell['ManaPerTurn']
                if 'Armor' in spell and time_left == 1:
                    player.armor -= spell['Armor']
                active_spells[name] -= 1

    def does_player_win_fight(
            self,
            player,
            boss,
            active_spells={},
            players_turn=True):
        if player.spent_mana >= self.max_spent:
            return player.spent_mana

        if players_turn and self.level == 'hard':
            player.hp -= 1
            if player.hp <= 0:
                return Solver.LARGE_SPENT

        self.process_spell_effects(player, boss, active_spells)
        if boss.hp <= 0:
            if player.spent_mana < self.max_spent:
                self.max_spent = player.spent_mana
            return player.spent_mana

        if players_turn:
            min_spent = Solver.LARGE_SPENT
            spell_cast = False
            # Try casting all possible spells, one at a time.
            for name, effect in Solver.spells.items():
                spell = Solver.spells[name]

                if name in active_spells and active_spells[name] > 0:
                    continue
                if spell['Cost'] > player.mana:
                    continue

                spell_cast = True

                # new_player = PlayerState(player.hp, player.mana,
                #                          player.armor, player.spent_mana)
                new_player = player.copy()
                new_boss = boss.copy()
                # new_boss = BossState(boss.hp, boss.damage)
                new_active_spells = active_spells.copy()

                new_player.mana -= spell['Cost']
                new_player.spent_mana += spell['Cost']

                if 'Armor' in spell:
                    new_player.armor += spell['Armor']
                if 'Damage' in spell:
                    new_boss.hp -= spell['Damage']
                if 'Heal' in spell:
                    new_player.hp += spell['Heal']
                if 'Duration' in spell and spell['Duration'] > 0:
                    new_active_spells[name] = spell['Duration']

                spent = self.does_player_win_fight(
                        new_player, new_boss, new_active_spells,
                        not players_turn)
                if spent < min_spent:
                    min_spent = spent
            # Player can't afford spell and loses.
            if not spell_cast:
                # print("Player loses (can't afford any spell)")
                return Solver.LARGE_SPENT
        else:
            player.hp -= max(1, boss.damage - player.armor)
            if player.hp <= 0:
                # print("Player loses (out of HP)")
                return Solver.LARGE_SPENT

            min_spent = self.does_player_win_fight(
                    player, boss, active_spells, not players_turn)
        return min_spent

    def solve(self):
        """Solution for part one or part two."""
        boss_stats = self.as_dict()
        for key, val in boss_stats.items():
            boss_stats[key] = int(val)

        player = PlayerState(50, 500)
        boss = BossState(boss_stats['Hit Points'], boss_stats['Damage'])
        return self.does_player_win_fight(player, boss)


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
