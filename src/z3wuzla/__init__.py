import z3
import bitwuzla
print("Hello from z3wuzla!")

tm = bitwuzla.TermManager()
options = bitwuzla.Options()
options.set(bitwuzla.Option.PRODUCE_MODELS, True)
parser = bitwuzla.Parser(tm, options)

def wuzl_check(solver: z3.Solver, *assumptions):
    if len(assumptions) > 0:
        print("Assumptions are currently unsupported")
    print("I wuzled your check")
    smt2string = solver.to_smt2()
    parser.parse(smt2string, True, False)

    return parser.bitwuzla().check_sat()

z3.Solver.check = wuzl_check
