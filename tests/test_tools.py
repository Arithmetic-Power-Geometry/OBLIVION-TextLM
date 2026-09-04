from oblivion_textlm.tools.calculator import CalculatorTool
from oblivion_textlm.tools.registry import ToolRegistry



def test_tool_registry_and_calculator():
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    result = registry.call("calculator", {"expression": "2 + 3 * 4"})
    assert result.ok
    assert result.output == "14"
