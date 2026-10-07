import ast
import pathlib
import unittest

ROOT = pathlib.Path(__file__).parents[1]
SOURCE = (ROOT / "server/main.py").read_text(encoding="utf-8")


class ServerTests(unittest.TestCase):
    def test_tools_and_transport_are_declared(self):
        tree = ast.parse(SOURCE)
        decorated = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for decorator in node.decorator_list if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute) and decorator.func.attr == "tool"}
        self.assertEqual(decorated, {"ask_model", "generate_image", "list_models"})
        self.assertIn('mcp.run(transport="stdio")', SOURCE)
        self.assertNotIn("videos/generations", SOURCE)

    def test_request_safety_boundaries(self):
        self.assertIn("User-Agent", SOURCE)
        self.assertIn("timeout=60", SOURCE)
        self.assertIn("MODEL_API_KEY", SOURCE)
        self.assertNotIn("sk-", SOURCE)
        self.assertNotIn("/v1/" + "tasks", SOURCE)

    def test_no_import_time_request(self):
        tree = ast.parse(SOURCE)
        top_level_calls = {
            node.func.id
            for node in tree.body
            if isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
        }
        self.assertNotIn("urlopen", top_level_calls)


if __name__ == "__main__":
    unittest.main()
