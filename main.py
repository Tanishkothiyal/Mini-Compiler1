# from lexer import tokenize
# from parser_ast import Parser
# from icg import generate_code
# from optimizer import optimize
# from visualize_ast import visualize


# def main():

#     # Ask user for file name
#     filename = input("Enter source file name (.txt / .java): ")

#     # Read source code
#     code = open(filename).read()

#         # Extract expression after '=' if present
#     if "=" in code:
#         code = code.split("=")[1]

# # Remove semicolon
#     code = code.replace(";", "")

#     # Tokenization
#     tokens = tokenize(code)

#     print("\nTOKENS")
#     for t in tokens:
#         print(t)

#     # Parsing and AST
#     parser = Parser(tokens)
#     ast = parser.parse()

#     print("\nAST GENERATED")

#     # Visualize AST
#     visualize(ast)

#     # Intermediate Code
#     intermediate_code = []
#     generate_code(ast, intermediate_code)

#     print("\nINTERMEDIATE CODE")
#     for line in intermediate_code:
#         print(line)

#     # Optimization
#     optimized = optimize(intermediate_code)

#     print("\nOPTIMIZED CODE")
#     for line in optimized:
#         print(line)


# if __name__ == "__main__":
#     main()

from lexer import tokenize
from parser_ast import Parser
from icg import generate_code
from optimizer import optimize
from visualize_ast import visualize
from Symbol_table import add_symbol, print_symbol_table


def main():

    filename = input("Enter source file name (.java / .txt): ")

    try:
        code = open(filename).read()
    except FileNotFoundError:
        print("File not found")
        return

    print("\nSOURCE CODE\n")
    print(code)

    lines = code.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Handle variable declaration
        if line.startswith("int"):
            parts = line.replace(";", "").split()

            if len(parts) >= 2:
                var_name = parts[1]
                add_symbol(var_name, "int")

        # Handle assignment
        if "=" in line:
            expr = line.split("=")[1]
            expr = expr.replace(";", "").strip()

            print("\nProcessing Expression:", expr)

            tokens = tokenize(expr)
            print("TOKENS:", tokens)

            parser = Parser(tokens)
            ast = parser.parse()

            visualize(ast)

            intermediate_code = []
            generate_code(ast, intermediate_code)

            print("INTERMEDIATE CODE:")
            for line in intermediate_code:
                print(line)

            optimized = optimize(intermediate_code)

            print("OPTIMIZED CODE:")
            for line in optimized:
                print(line)

    # Print Symbol Table
    print_symbol_table()


if __name__ == "__main__":
    main()