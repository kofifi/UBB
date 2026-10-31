from ortools.math_opt.python import mathopt


def main() -> None:
    S = {1,2,3,4,5,6}
    C = [{1,2,5}, {2,3,4}, {1,4,6}, {1,3,5}, {2,4,6}, {3,5,6}]

    n = len(S)
    m = len(C)

    model = mathopt.Model(name="Zad1")

    x = [model.add_binary_variable(name=f"x[{i}]") for i in range(m)]

    for i in S:
         model.add_linear_constraint(sum(x[j] for j in range(m) if i in C[j]) <= 1, name=f"cover_{i}")

    model.maximize(sum(x[j] for j in range(m)))

    result = mathopt.solve(model, mathopt.SolverType.GSCIP)
    if result.termination.reason != mathopt.TerminationReason.OPTIMAL:
        raise RuntimeError(f"model failed to solve: {result.termination}")

    values = result.variable_values()
    chosen = [j for j in range(m) if values[x[j]] > 0.5]

    print("Status:", result.termination.reason.name)
    print("Liczba wybranych zbiorow:", round(result.objective_value()))
    for j in chosen:
        print(f"  C[{j}] = {sorted(C[j])}")

if __name__ == "__main__":
    main()



