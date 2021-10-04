"""
Usage in docker: docker-compose exec web python tests/get_recipe_detail_test.py
"""
import unittest
import responses
from src.spoon import getRecipeById


class TestGetRecipeById(unittest.TestCase):
    @responses.activate
    def testGetRecipeByID(self):
        expected_request_url = 'https://api.spoonacular.com/recipes/12345/information?&apiKey=9e749e7df97047c38000f0f4addb64f9'
        responses.add(responses.GET, expected_request_url, json={'title': 'Morning Glory Muffins'}, status=200)

        resp = getRecipeById(12345)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_request_url
        assert resp['title'] == 'Morning Glory Muffins'

    @responses.activate
    def test404NotFound(self):
        expected_request_url = 'https://api.spoonacular.com/recipes/54321/information?&apiKey=9e749e7df97047c38000f0f4addb64f9'
        responses.add(responses.GET, expected_request_url, json={'error': 'not found'}, status=404)

        resp = getRecipeById(54321)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == expected_request_url
        assert resp == {"error": "not found"}


if __name__ == '__main__':
    unittest.main()
