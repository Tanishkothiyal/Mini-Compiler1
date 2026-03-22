def optimize(code):

    optimized = []

    for line in code:

        left, expr = line.split('=')

        left = left.strip()
        expr = expr.strip()

        parts = expr.split()

        if parts[0].isdigit() and parts[2].isdigit():

            if parts[1] == '+':
                result = int(parts[0]) + int(parts[2])
            elif parts[1] == '-':
                result = int(parts[0]) - int(parts[2])
            elif parts[1] == '*':
                result = int(parts[0]) * int(parts[2])
            elif parts[1] == '/':
                result = int(parts[0]) // int(parts[2])

            optimized.append(f"{left} = {result}")

        else:
            optimized.append(line)

    return optimized