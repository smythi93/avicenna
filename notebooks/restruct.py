import string
import math
import logging

from fuzzingbook.Grammars import Grammar
from isla.language import DerivationTree
from isla.language import ISLaUnparser, Formula

from avicenna import Avicenna
from avicenna.oracle import OracleResult
from avicenna.input import Input


grammar: Grammar = {
    "<start>": ["<arith_expr>"],
    "<arith_expr>": ["<function>(<number>)"],
    "<function>": ["sqrt", "sin", "cos", "tan"],
    "<number>": ["<maybe_minus><onenine><maybe_digits><maybe_frac>"],
    "<maybe_minus>": ["", "-"],
    "<onenine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
    "<maybe_frac>": ["", ".<digits>"],
}

initial_inputs = ["cos(10)", "sqrt(28367)", "tan(-12)", "sqrt(-900)"]


def arith_eval(inp) -> float:
    return eval(
        str(inp), {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan}
    )


def oracle(inp: Input) -> OracleResult:
    try:
        arith_eval(inp)
        return OracleResult.NO_BUG
    except ValueError:
        return OracleResult.BUG


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:  %(message)s")

    # from avicenna_formalizations.heartbeat import grammar, initial_inputs, prop as oracle
    avicenna = Avicenna(
        grammar=grammar,
        initial_inputs=initial_inputs,
        oracle=oracle,
        max_iterations=10,
    )

    result = avicenna.execute()

    print(ISLaUnparser(result[0][0]).unparse())