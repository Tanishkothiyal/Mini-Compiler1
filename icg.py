temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"


def generate_code(node, code):

    if node.left is None and node.right is None:
        return node.value

    left = generate_code(node.left, code)
    right = generate_code(node.right, code)

    temp = new_temp()

    code.append(f"{temp} = {left} {node.value} {right}")

    return temp