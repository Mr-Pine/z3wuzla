import z3
import bitwuzla

from .constant import get_const_interp
from .function import extract_lambda
from .nops import nop1, nop2

print("Hello from z3wuzla!")

tm = bitwuzla.TermManager()
options = bitwuzla.Options()
options.set(bitwuzla.Option.PRODUCE_MODELS, True)
parser = bitwuzla.Parser(tm, options)


def get_consts():
    return [term for term in parser.get_declared_funs() if not term.sort().is_fun()]


def get_num_consts(_ctx, _model):
    return len(get_consts())


def get_const(idx):
    return get_consts()[idx]


def get_funcs():
    return [term for term in parser.get_declared_funs() if term.sort().is_fun()]


def get_num_funcs(_ctx, _model):
    return len(get_funcs())


def get_func(idx):
    return get_funcs()[idx]


def get_arity(_ctx, func):
    if not func.sort().is_fun():
        return 0
    return len(func.sort().fun_domain())


def get_item(self, idx):
    if isinstance(idx, int):
        if idx >= len(self):
            raise IndexError
        num_consts = get_num_consts(self.ctx.ref(), self.model)
        if idx < num_consts:
            ref = z3.FuncDeclRef(get_const(idx), self.ctx)
        else:
            ref = z3.FuncDeclRef(get_func(idx - num_consts), self.ctx)
        ref.as_ast = nop1.__get__(ref)
        return ref
    elif isinstance(idx, z3.FuncDeclRef):
        return self.get_interp(idx)
    else:
        raise Exception("Unsupported index")


def wuzl_model(self: z3.Solver):
    print("I wuzled your model")
    model = MyModel()
    model_ref = z3.ModelRef(model, z3.main_ctx())

    return model_ref


class MyModel:
    pass


def wuzl_check(self: z3.Solver, *assumptions):
    if len(assumptions) > 0:
        print("Assumptions are currently unsupported")
    print("I wuzled your check")
    smt2string = self.to_smt2()
    parser.parse(smt2string, True, False)

    res = parser.bitwuzla().check_sat()

    self.model = wuzl_model.__get__(self)

    if res == bitwuzla.Result.SAT:
        return z3.sat
    elif res == bitwuzla.Result.UNSAT:
        return z3.unsat
    else:
        return z3.unknown


z3.Solver.check = wuzl_check
z3.z3.Z3_model_inc_ref = nop2
z3.z3.Z3_model_dec_ref = None
z3.z3.Z3_model_get_num_consts = get_num_consts
z3.z3.Z3_model_get_num_funcs = get_num_funcs
z3.z3.ModelRef.__getitem__ = get_item

old_inc_ref = z3.z3.Z3_inc_ref


def inc_ref(ctx_ref, ref):
    if isinstance(ref, bitwuzla.Term):
        return
    else:
        return old_inc_ref(ctx_ref, ref)


z3.z3.Z3_inc_ref = inc_ref

old_func_decl_as_ast = z3.z3.FuncDeclRef.as_ast


def new_as_ast(self):
    if isinstance(self.ast, bitwuzla.Term):
        return self.ast
    else:
        return old_func_decl_as_ast(self)


z3.z3.FuncDeclRef.as_ast = new_as_ast
z3.z3.Z3_get_arity = get_arity

z3.z3.Z3_model_get_func_interp = extract_lambda.__get__(parser)
z3.z3.Z3_model_get_const_interp = get_const_interp.__get__(parser)

old_op_name = z3.z3printer._op_name


def new_op_name(expr):
    if isinstance(expr, bitwuzla.Term):
        return expr.symbol()
    elif hasattr(expr, "ast") and isinstance(expr.ast, bitwuzla.Term):
        return expr.ast.symbol()
    else:
        return old_op_name(expr)


z3.z3printer._op_name = new_op_name
