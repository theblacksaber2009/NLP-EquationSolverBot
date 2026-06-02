seq_train = [
    [1, 2, 3, 4], [5, 10, 15, 20], [0, -2, -4, -6], [10, 8, 6, 4],
    [1, 2, 4, 8], [3, 6, 12, 24], [2, 4, 8, 16], [5, 10, 20, 40],
    [1, 4, 9, 16], [4, 9, 16, 25], [9, 16, 25, 36],
    [1, 8, 27, 64], [8, 27, 64, 125],
    [1, 1, 2, 3], [2, 3, 5, 8], [3, 5, 8, 13],
    [2, 4, 8, 16], [3, 9, 27, 81], [5, 25, 125, 625]
]

seq_labels = [
    5, 25, -8, 2,
    16, 48, 32, 80,
    25, 36, 49,
    125, 216,
    5, 13, 21,
    32, 243, 3125
]

game_inputs = [
    ["rock", "paper"],
    ["paper", "scissors"],
    ["scissors", "rock"]
]

game_outputs = ["scissors", "rock", "paper"]

# Add decreasing arithmetic
for start in range(20, 4, -1):
    seq = [start - i for i in range(4)]
    seq_train.append(seq)
    seq_labels.append(start - 4)

# Add increasing arithmetic
for start in range(1, 15):
    seq = [start + i for i in range(4)]
    seq_train.append(seq)
    seq_labels.append(start + 4)

# Add geometric patterns
for base in range(1, 5):
    seq = [base * (2 ** i) for i in range(4)]
    seq_train.append(seq)
    seq_labels.append(base * (2 ** 4))

# Add squares
for i in range(1, 10):
    seq = [j**2 for j in range(i, i+4)]
    seq_train.append(seq)
    seq_labels.append((i+4)**2)

# Add cubes
for i in range(1, 6):
    seq = [j**3 for j in range(i, i+4)]
    seq_train.append(seq)
    seq_labels.append((i+4)**3)

# Add Fibonacci
fibo = [1, 1, 2, 3, 5, 8, 13, 21, 34]
for i in range(len(fibo) - 4):
    seq = fibo[i:i+4]
    seq_train.append(seq)
    seq_labels.append(fibo[i+4])

