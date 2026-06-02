from sklearn.tree import DecisionTreeClassifier

class GameBot:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.trained = False

    def encode(self, move):
        return {"rock": 0, "paper": 1, "scissors": 2}[move]

    def decode(self, value):
        return ["rock", "paper", "scissors"][value]

    def train(self, history_inputs, next_moves):
        X = [[self.encode(p), self.encode(b)] for p, b in history_inputs]
        y = [self.encode(n) for n in next_moves]
        self.model.fit(X, y)
        self.trained = True

    def predict(self, last_player_move, last_bot_move):
        if not self.trained:
            return "Model not trained."
        try:
            x = [[self.encode(last_player_move), self.encode(last_bot_move)]]
            pred = self.model.predict(x)[0]
            return self.decode(pred)
        except:
            return "Invalid input."
