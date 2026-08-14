import ast
import operator

class SafeEvaluator:
    """
    Bezpieczny ewaluator warunków dla grafu. Zastępuje niebezpieczny eval() 
    drzewem AST, pozwalając na proste instrukcje logiczne i matematyczne, 
    bez ryzyka wykonania dowolnego kodu (Arbitrary Code Execution).
    """
    
    ALLOWED_OPERATORS = {
        ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
        ast.Pow: operator.pow, ast.Eq: operator.eq, ast.NotEq: operator.ne,
        ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt,
        ast.GtE: operator.ge, ast.BitAnd: operator.and_, ast.BitOr: operator.or_,
        ast.USub: operator.neg, ast.Not: operator.not_, ast.And: lambda a, b: a and b,
        ast.Or: lambda a, b: a or b
    }

    @classmethod
    def evaluate(cls, condition: str, state: dict) -> bool:
        if not condition:
            return True
            
        try:
            tree = ast.parse(condition, mode='eval').body
            return bool(cls._eval_node(tree, state))
        except Exception as e:
            print(f"[EVALUATOR] Failed to evaluate condition '{condition}': {e}")
            return False

    @classmethod
    def _eval_node(cls, node, state: dict):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Constant): # Python 3.8+
            return node.value
        elif isinstance(node, ast.Name):
            if node.id in state:
                return state[node.id]
            if node.id == "true":
                return True
            if node.id == "false":
                return False
            raise ValueError(f"Unknown variable in state: {node.id}")
        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left, state)
            right = cls._eval_node(node.right, state)
            return cls.ALLOWED_OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.Compare):
            left = cls._eval_node(node.left, state)
            for op, comparator in zip(node.ops, node.comparators):
                right = cls._eval_node(comparator, state)
                if not cls.ALLOWED_OPERATORS[type(op)](left, right):
                    return False
                left = right
            return True
        elif isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                return all(cls._eval_node(v, state) for v in node.values)
            elif isinstance(node.op, ast.Or):
                return any(cls._eval_node(v, state) for v in node.values)
        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand, state)
            return cls.ALLOWED_OPERATORS[type(node.op)](operand)
            
        raise TypeError(f"Unsupported AST node type: {type(node)}")
