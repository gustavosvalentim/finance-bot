from typing import List, Type, Any
from importlib import import_module

class ClassLoadingError(Exception):
    """Raised when class loading fails"""
    pass

class ClassLoader:
    @classmethod
    def load_class(cls, class_path: str) -> Type[Any]:
        """Load a class from string path with validation"""
        try:
            module_name, class_name = class_path.rsplit('.', 1)
            module = import_module(module_name)
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            raise ClassLoadingError(f"Failed to load class {class_path}: {e}")
    
    @classmethod
    def instantiate_classes(cls, class_paths: List[str]) -> List[Any]:
        """Load and instantiate multiple classes"""
        instances = []
        for class_path in class_paths:
            try:
                class_obj = cls.load_class(class_path)
                instance = class_obj()
                instances.append(instance)
            except Exception as e:
                raise ClassLoadingError(f"Failed to instantiate {class_path}: {e}")
        return instances
