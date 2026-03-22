from lexer import tokenize
from parser_ast import Parser
from icg import generate_code
from optimizer import optimize
from visualize_ast import visualize


def main():

    # Ask user for file name
    filename = input("Enter source file name (.txt / .java): ")

    # Read source code
    code = open(filename).read()

        # Extract expression after '=' if present
    if "=" in code:
        code = code.split("=")[1]

# Remove semicolon
    code = code.replace(";", "")

    # Tokenization
    tokens = tokenize(code)

    print("\nTOKENS")
    for t in tokens:
        print(t)

    # Parsing and AST
    parser = Parser(tokens)
    ast = parser.parse()

    print("\nAST GENERATED")

    # Visualize AST
    visualize(ast)

    # Intermediate Code
    intermediate_code = []
    generate_code(ast, intermediate_code)

    print("\nINTERMEDIATE CODE")
    for line in intermediate_code:
        print(line)

    # Optimization
    optimized = optimize(intermediate_code)

    print("\nOPTIMIZED CODE")
    for line in optimized:
        print(line)


if __name__ == "__main__":
    main()