import bitwuzla
import z3
from .nops import nop2
from .values import bitwuzla_to_z3

def extract_lambda(parser: bitwuzla.Parser, _1, _2, term_decl):
    term = parser.bitwuzla().get_value(term_decl)
    parameters = []
    while term.kind() == bitwuzla.Kind.LAMBDA:
        parameters.append(term[0])
        term = term[1]

    definitions = []

    while term.kind() == bitwuzla.Kind.ITE:
        args = [None] * len(parameters)
        input_term = term[0]
        while input_term.kind() == bitwuzla.Kind.AND:
            input = input_term[0]
            input_term = input_term[1]
            assert(input.kind() == bitwuzla.Kind.EQUAL)
            param = input[0]
            param_index = parameters.index(param)
            value = input[1]
            args[param_index] = value
        assert(input_term.kind() == bitwuzla.Kind.EQUAL)
        param = input_term[0]
        param_index = parameters.index(param)
        value = input_term[1]
        args[param_index] = value

        definitions.append((args, term[1]))
        term = term[2]

    return (definitions, term)

def get_num_func_entries(_ctx, func):
    return len(func[0])

def get_func_entry(_ctx, func, idx):
    return func[0][idx]

def get_func_else(_ctx, func):
    return func[1]

def get_func_num_args(_ctx, entry):
    return len(entry[0])

def get_func_entry_arg(_ctx, entry, idx):
    return entry[0][idx]

def get_func_entry_value(_ctx, entry):
    return entry[1]

z3.z3.Z3_func_interp_inc_ref = nop2
z3.z3.Z3_func_interp_dec_ref = nop2
z3.z3.Z3_func_interp_get_num_entries = get_num_func_entries
z3.z3.Z3_func_interp_get_entry = get_func_entry
z3.z3.Z3_func_entry_inc_ref = nop2
z3.z3.Z3_func_entry_dec_ref = nop2
z3.z3.Z3_func_entry_get_num_args = get_func_num_args
z3.z3.Z3_func_entry_get_arg = get_func_entry_arg
z3.z3.Z3_func_entry_get_value = get_func_entry_value
z3.z3.Z3_func_interp_get_else = get_func_else
