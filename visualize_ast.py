from graphviz import Digraph


def visualize(node):

    dot = Digraph()

    def add_nodes(n):

        if n is None:
            return

        dot.node(str(id(n)), str(n.value))

        if n.left:
            dot.edge(str(id(n)), str(id(n.left)))
            add_nodes(n.left)

        if n.right:
            dot.edge(str(id(n)), str(id(n.right)))
            add_nodes(n.right)

    add_nodes(node)

    dot.render("ast_tree", view=False, format="png")