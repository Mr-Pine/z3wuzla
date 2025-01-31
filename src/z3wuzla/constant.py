import bitwuzla
def get_const_interp(parser: bitwuzla.Parser, _ctx, model, const):
    res = parser.bitwuzla().get_value(const)
    print("constant", res)
    return res
