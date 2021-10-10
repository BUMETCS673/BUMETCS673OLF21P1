"""
Usage in docker: docker-compose exec web python tests/getRecipeDetail_unittest.py
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import responses
from spoon import getRecipeDetail

class TestGetRecipeDetail(unittest.TestCase):
    @responses.activate
    def testGetRecipeDetail(self):
        expected_request_url = 'https://api.spoonacular.com/recipes/12345/information?&apiKey=9e749e7df97047c38000f0f4addb64f9'
        responses.add(responses.GET, expected_request_url, json={'title': 'Morning Glory Muffins'}, status=200)

        resp = getRecipeDetail(12345)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_request_url
        assert resp['title'] == 'Morning Glory Muffins'

    @responses.activate
    def test404NotFound(self):
        expected_request_url = 'https://api.spoonacular.com/recipes/54321/information?&apiKey=9e749e7df97047c38000f0f4addb64f9'
        responses.add(responses.GET, expected_request_url, json={'error': 'not found'}, status=404)

        resp = getRecipeDetail(54321)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_request_url
        assert resp == {"error": "not found"}


if __name__ == '__main__':
    unittest.main()
