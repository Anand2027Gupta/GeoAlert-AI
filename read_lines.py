with open('model.py', 'r') as f:
    lines = f.readlines()
    for i in range(1060, 1110):
        print(f"{i+1}: {lines[i]}", end='')