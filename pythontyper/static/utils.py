import ast

def is_variable(node):
    # Check if the node is an instance of ast.Name
    if not isinstance(node, ast.Name):
        return False
    
    # Check if the node is used as a target in assignment or loop
    parent = node.ctx
    return (
        isinstance(parent, (ast.Assign, ast.AnnAssign, ast.For, ast.Store))
    )