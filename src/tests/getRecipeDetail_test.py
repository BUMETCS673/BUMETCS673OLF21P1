"""
Usage in docker: docker-compose exec web python tests/getRecipeDetail_test.py
"""

import unittest
import responses
from src.spoon import get_recipe_by_id