import os
import sys

# Inserta .../<repo>/src al inicio del sys.path para que pytest vea "app"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
