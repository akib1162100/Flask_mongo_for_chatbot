import os
# import importlib

module_path = os.path.dirname(os.path.abspath(__file__))
repository = [
    f for f in os.listdir(module_path) if f.endswith(".py") and f != "__init__.py"
]
__all__ = repository

# for repo in repository:
#     importlib.import_module("controllers.%s" % repo[:-2])

print(
    "Imported repository: %s" % ", ".join(repository)
    if repository
    else "No repository avaiable in the repository directory."
)