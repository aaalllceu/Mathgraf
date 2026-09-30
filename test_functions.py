import ast
import pathlib
import sys
import unittest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from function_math import evaluate, quadratic_characteristics

SOURCE = PROJECT_ROOT / "main.py"


class FunctionMathTests(unittest.TestCase):
    def test_application_source_is_valid_python(self):
        ast.parse(SOURCE.read_text(encoding="utf-8"))

    def test_linear_function(self):
        self.assertEqual(evaluate("linear", (2.0, -3.0, 0.0), 4), 5.0)
        self.assertEqual(evaluate("linear", (2.0, -3.0, 0.0), 0), -3.0)

    def test_quadratic_function(self):
        self.assertEqual(evaluate("quadratic", (1.0, -4.0, 3.0), 1), 0.0)
        self.assertEqual(evaluate("quadratic", (1.0, -4.0, 3.0), 3), 0.0)

    def test_quadratic_vertex_and_roots(self):
        self.assertEqual(quadratic_characteristics(1.0, -4.0, 3.0), (4.0, 2.0, -1.0, "duas raízes reais"))

    def test_quadratic_double_root(self):
        delta, _, _, roots = quadratic_characteristics(1, 2, 1)
        self.assertEqual(delta, 0)
        self.assertEqual(roots, "uma raiz real")

    def test_quadratic_without_real_roots(self):
        delta, _, _, roots = quadratic_characteristics(1, 0, 1)
        self.assertLess(delta, 0)
        self.assertEqual(roots, "sem raízes reais")

    def test_rejects_zero_quadratic_coefficient(self):
        with self.assertRaises(ValueError):
            quadratic_characteristics(0, 2, 1)

    def test_rejects_unknown_function_mode(self):
        with self.assertRaises(ValueError):
            evaluate("cubic", (1, 0, 0), 2)


if __name__ == "__main__":
    unittest.main()
