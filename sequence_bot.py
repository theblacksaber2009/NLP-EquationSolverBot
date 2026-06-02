from sklearn.ensemble import RandomForestRegressor
import math

class SmartSequenceBot:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=200)
        self.trained = False

    def train(self, sequences, labels):
        self.model.fit(sequences, labels)
        self.trained = True

    def is_arithmetic(self, seq):
        diff = seq[1] - seq[0]
        return all(seq[i+1] - seq[i] == diff for i in range(len(seq)-1)), diff

    def is_geometric(self, seq):
        if 0 in seq:
            return False, 0
        ratio = seq[1] / seq[0]
        return all(abs(seq[i+1] / seq[i] - ratio) < 1e-6 for i in range(len(seq)-1)), ratio


    def is_square_sequence(self, seq):
        return all(int(math.sqrt(n))**2 == n for n in seq), "square"

    def is_cube_sequence(self, seq):
        return all(round(n**(1/3))**3 == n for n in seq), "cube"

    def analyze(self, seq):
        if not self.trained:
            return "Model not trained."
        if len(seq) != 4:
            return "Enter exactly 4 numbers."

        is_arith, diff = self.is_arithmetic(seq)
        if is_arith:
            return seq[-1] + diff

        is_geom, ratio = self.is_geometric(seq)
        if is_geom:
            return round(seq[-1] * ratio)

        is_square, _ = self.is_square_sequence(seq)
        if is_square:
            return (int(math.sqrt(seq[-1])) + 1) ** 2

        is_cube, _ = self.is_cube_sequence(seq)
        if is_cube:
            return (round(seq[-1] ** (1/3)) + 1) ** 3

        prediction = self.model.predict([seq])[0]
        return int(prediction + 0.5)

