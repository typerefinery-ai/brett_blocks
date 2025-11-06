"""
Brett Blocks Test Package
Comprehensive testing framework for STIX data form conversion and object creation
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import commonly used testing utilities
from .utils.test_helpers import *
from .utils.stix_utils import *
from .utils.data_form_utils import *