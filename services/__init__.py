import os

module_path = os.path.dirname(os.path.abspath(__file__))
services = [
    f for f in os.listdir(module_path) if f.endswith(".py") and f != "__init__.py"
]
__all__ = services
print(
    "Imported services: %s" % ", ".join(services)
    if services
    else "No services avaiable in the services directory."
)
