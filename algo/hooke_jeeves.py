import sympy, os
from algo.miscalc_number import MiscalcNumber
from algo.wrong_size_error import WrongSizeError

def from_miscalc(v):
    v = v.copy()
    for name in v.keys():
        v[name] = v[name].number
    return v

MAX_ITERATIONS = 100

def execute(var_names, funct, eps=1e-4, a=2, lam=1.01, steps=[1e-3, 1e-3], starting_point=[-4, -4]):
    n = len(var_names)
    if len(steps) != len(starting_point) or len(steps) != n or n == 0:
        raise WrongSizeError
    val_dict = dict()
    for name, val in zip(var_names, starting_point):
        val_dict[name] = MiscalcNumber(val)
    f0 = funct.subs(from_miscalc(val_dict))
    lam = MiscalcNumber(lam)
    a = MiscalcNumber(a)
    steps=[MiscalcNumber(i) for i in steps]
    its = 0

    while max([i.number for i in steps]) >= eps:
        its += 1
        if its > MAX_ITERATIONS:
            break
        cur_dict = val_dict.copy()
        cur = -1
        current_f = f0
        for name in cur_dict:
            cur += 1
            val = cur_dict[name]
            base = val
            cur_dict[name] = base + steps[cur]
            if funct.subs(from_miscalc(cur_dict)) < current_f:
                current_f = funct.subs(from_miscalc(cur_dict))
                continue
            cur_dict[name] = base - steps[cur]
            if funct.subs(from_miscalc(cur_dict)) < current_f:
                current_f = funct.subs(from_miscalc(cur_dict))
                continue
            cur_dict[name] = base
        if current_f < f0:
            for name in val_dict:
                cur_dict[name] += lam * (cur_dict[name] - val_dict[name])
            val_dict = cur_dict
            f0 = current_f
            continue
        for step in steps:
            if step.number > eps:
                step /= a
    return val_dict


if __name__ == "__main__":
    x1, x2 = sympy.symbols('x1 x2')
    f = 5 * x1**6 + x1**5 + x1**4 - x1**3 + x1**2 + x1 - 3 + x2**6 - 3 * x2**5 + x2**4 + x2**3 + x2**2 + x2 + 4
    res = execute(['x1', 'x2'], f)
    for name in res: 
        print(f"{name} = {res[name]}")
