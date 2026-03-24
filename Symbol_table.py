symbol_table = {}

def add_symbol(name, datatype):
    symbol_table[name] = datatype

def print_symbol_table():
    print("\nSYMBOL TABLE")
    print("Variable  ->  Type")
    for var, dtype in symbol_table.items():
        print(f"{var} -> {dtype}")