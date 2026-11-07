from math import prod

from ortools.math_opt.python import mathopt

NUMBERS = [
    641, 4112, 3296, 3146, 1716, 1521, 5566, 6600, 831875, 6318, 1242, 2827, 324, 250,
    17303, 1782, 345, 352, 4950, 3125, 28561, 5175, 3300, 3399, 12167, 1170, 2369, 3312,
    330, 1542, 5070, 515, 164737, 3042, 6210, 2340, 5769, 288, 1285, 744769, 23,
]
TARGET = 58503359928829676889083701609993243500000


def factorize(n: int) -> dict[int, int]:
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def main() -> None:
    factors = [factorize(a) for a in NUMBERS]
    primes = sorted({p for f in factors for p in f})

    rest = TARGET
    exponents = {}
    for p in primes:
        exponents[p] = 0
        while rest % p == 0:
            rest //= p
            exponents[p] += 1

    if rest != 1:
        print("Odpowiedz: NIE")
        print(f"Czynnik {rest} nie wystepuje w zadnej liczbie ze zbioru")
        return

    n = len(NUMBERS)

    model = mathopt.Model(name="Zad18")

    x = [model.add_binary_variable(name=f"x[{i}]") for i in range(n)]

    for p in primes:
        model.add_linear_constraint(
            sum(factors[i].get(p, 0) * x[i] for i in range(n)) == exponents[p],
            name=f"prime_{p}",
        )

    result = mathopt.solve(model, mathopt.SolverType.GSCIP)
    if result.termination.reason == mathopt.TerminationReason.INFEASIBLE:
        print("Status:", result.termination.reason.name)
        print("Odpowiedz: NIE")
        return
    if result.termination.reason != mathopt.TerminationReason.OPTIMAL:
        raise RuntimeError(f"model failed to solve: {result.termination}")

    values = result.variable_values()
    chosen = [NUMBERS[i] for i in range(n) if values[x[i]] > 0.5]

    if prod(chosen) != TARGET:
        raise RuntimeError("product of chosen numbers does not match the target")

    print("Status:", result.termination.reason.name)
    print("Odpowiedz: TAK")
    print("Liczba wybranych liczb:", len(chosen))
    print("Podzbior:", sorted(chosen))
    print("Iloczyn:", prod(chosen))


if __name__ == "__main__":
    main()
