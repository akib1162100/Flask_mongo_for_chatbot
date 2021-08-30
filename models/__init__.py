import os
import importlib

module_path = os.path.dirname(os.path.abspath(__file__))
models = [
    f for f in os.listdir(module_path) if f.endswith(".py") and f != "__init__.py"
]
for view in models:
    importlib.import_module("models.%s" % view[:-3])


__all__ = models
print(
    "Imported model: %s" % ", ".join(models)
    if models
    else "No models avaiable in the model directory."
)
