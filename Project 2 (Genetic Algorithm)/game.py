class Game:
    def __init__(self, levels):

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def get_score(self, actions):

        current_level = self.levels[self.current_level_index]
        steps = 0
        points = 0
        scores = 0
        for i in range(self.current_level_len - 1):
            current_step = current_level[i]
            if current_step == '_':
                steps += 1
            elif current_step == 'G' and actions[i - 1] == '1' and actions[i - 2] != '1':
                steps += 1
            elif current_step == 'L' and actions[i - 1] == '2' and actions[i - 2] != '1':
                steps += 1
            elif current_step == 'M':
                steps += 1
                if actions[i-1] == '0' or actions[i-1] == '2':
                    points += 2
            else:
                if steps > scores:
                    scores = steps
                steps = 0
        return steps == self.current_level_len - 1, points + max(steps, scores)


g = Game(["___M____MGM________M_M______M____L___G____M____L__G__GM__L____ML__G___G___L___G__G___M__L___G____M__"])
g.load_next_level()

# print(g.get_score("1021002210101000000021021000010222101020101020210100101020102220210001010200010210102022202100010101"))
