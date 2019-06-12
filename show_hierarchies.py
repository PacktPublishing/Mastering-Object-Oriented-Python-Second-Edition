"""
Create ASCII Art for hierarchies

Uses asciitree. https://pypi.org/project/asciitree/0.3.3/
"""

from asciitree import LeftAligned
from asciitree.drawing import BOX_HEAVY

rendering = LeftAligned()
rendering.draw.gfx = BOX_HEAVY

simple = {
    'module.py': {
        'class A:': {'def method(self): ...': {}},
        'class B:': {'def method(self): ...': {}},
        'def function():': {}}
}
print(rendering(simple))

package = {
    'package': {
        '__init__.py': {},
        'module1.py': {
            'class A:': {'def method(self): ...': {}},
            'def function():': {}},
        'module2.py': {'...': {}},
    }
}
print(rendering(package))

cpx = {
    'gemma': {
        'baseline': {'code.py': {}},
        'my-first-project': {'code.py': {}},
        'another-project': {'code.py': {}},
        'os-upgrade': {'other files...': {}}
    }
}
print(rendering(cpx))
