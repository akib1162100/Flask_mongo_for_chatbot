import os
import importlib

module_path = os.path.dirname(os.path.abspath(__file__))
controllers = [
    f for f in os.listdir(module_path) if f.endswith(".py") and f != "__init__.py"]

__all__ = controllers
for view in controllers:
    importlib.import_module("controllers.%s" % view[:-3])

print(
    "Imported controllers: %s" % ", ".join(controllers)
    if controllers
    else "No controllers avaiable in the models directory."
)