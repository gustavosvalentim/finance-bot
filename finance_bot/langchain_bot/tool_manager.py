from importlib import import_module
from typing import List, Any, Type
from langchain.tools import BaseTool


class ToolLoadingError(Exception):
    """Exception raised when tool loading fails"""
    pass


class ToolManager:
    """Manages tool loading and instantiation"""

    _instance = None
    _tools = []

    @staticmethod
    def instance() -> 'ToolManager':
        if ToolManager._instance is None:
            ToolManager._instance = ToolManager()
        return ToolManager._instance

    def _get_class(self, class_path: str) -> Type[BaseTool]:
        module_name, class_name = class_path.rsplit('.', 1)
        module = import_module(module_name)
        return getattr(module, class_name)

    def _internal_load_tools(self, tool_list: List[str]) -> List[Type[BaseTool]]:
        tools = []

        for tool_class_path in tool_list:
            tool_class = self._get_class(tool_class_path)
            if tool_class is None:
                raise ToolLoadingError(f"Failed to load tool: {tool_class_path}")
            
            try:
                tool_instance = tool_class()
                self._tools.append(tool_instance)
            except Exception as e:
                raise ToolLoadingError(f"Failed to instantiate tool {tool_class_path}: {str(e)}")

        return tools
    
    def load_tools(self, tool_list: None | List[str] = None) -> List[Type[BaseTool]]:
        """Load and instantiate all configured tools"""

        if len(self._tools) == 0 or tool_list is not None:
            self._tools = self._internal_load_tools(tool_list)

        return self._tools
