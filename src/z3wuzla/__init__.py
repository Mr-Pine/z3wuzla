import z3
import bitwuzla
print("Hello from z3wuzla!")

tm = bitwuzla.TermManager()
options = bitwuzla.Options()
options.set(bitwuzla.Option.PRODUCE_MODELS, True)
parser = bitwuzla.Parser(tm, options)


def nop():
    pass
def nop1(a):
    pass
def nop2(a, b):
    pass

def get_num_consts(_ctx, _model):
    return len([term for term in parser.get_declared_funs() if term.is_const()])
def get_const(idx):
    res = [term for term in parser.get_declared_funs() if term.is_const()][idx]
    return res

def get_num_funcs(_ctx, _model):
    return len(parser.get_declared_funs()) - get_num_consts(_ctx, _model)
def get_func(idx):
    res = [term for term in parser.get_declared_funs() if not term.is_const()][idx]
    return res

def get_item(self, idx):
    if isinstance(idx, int):
        if idx >= len(self):
            raise IndexError
        num_consts = get_num_consts(self.ctx.ref(), self.model)
        if (idx < num_consts):
            ref = z3.FuncDeclRef(get_const(idx), self.ctx)
        else:
            ref = z3.FuncDeclRef(get_func(idx - num_consts), self.ctx)
        ref.as_ast = nop1.__get__(ref)
        return ref
    else:
        raise "Unsupported index"

def wuzl_model(solver: z3.Solver):
    print("I wuzled your model")
    model = MyModel()
    model_ref = z3.ModelRef(model, z3.main_ctx())

    return model_ref

class MyModel():
    pass

def wuzl_check(solver: z3.Solver, *assumptions):
    if len(assumptions) > 0:
        print("Assumptions are currently unsupported")
    print("I wuzled your check")
    smt2string = solver.to_smt2()
    parser.parse(smt2string, True, False)

    res = parser.bitwuzla().check_sat()

    solver.model = wuzl_model.__get__(solver)

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
    if (isinstance(ref, bitwuzla.Term)):
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
