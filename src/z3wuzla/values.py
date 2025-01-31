import bitwuzla
import z3

def bitwuzla_to_z3(term: bitwuzla.Term):
    assert(term.is_value())
    if term.sort().is_bool():
        return z3.BoolVal(term.is_true())
    elif term.sort().is_bv():
        return z3.BitVecVal(int(term.value(), 2), term.sort().bv_size())

old_to_expr_ref = z3.z3._to_expr_ref
def new_to_expr_ref(expr, ctx):
    if isinstance(expr, bitwuzla.Term):
        return bitwuzla_to_z3(expr)
    else:
        return old_to_expr_ref(expr, ctx)
z3.z3._to_expr_ref = new_to_expr_ref
