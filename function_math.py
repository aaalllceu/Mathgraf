"""Funções matemáticas independentes da interface gráfica."""


def evaluate(mode, coefficients, x):
    """Calcula f(x) para os modos ``linear`` e ``quadratic``."""
    a, b, c = coefficients
    if mode == "linear":
        return a * x + b
    if mode == "quadratic":
        return a * x * x + b * x + c
    raise ValueError(f"Tipo de função desconhecido: {mode}")


def quadratic_characteristics(a, b, c):
    """Retorna discriminante, vértice e número de raízes reais."""
    if a == 0:
        raise ValueError("Na função do 2º grau, o coeficiente a não pode ser zero.")
    delta = b * b - 4 * a * c
    xv = -b / (2 * a)
    yv = evaluate("quadratic", (a, b, c), xv)
    roots = "duas raízes reais" if delta > 0 else "uma raiz real" if delta == 0 else "sem raízes reais"
    return delta, xv, yv, roots
