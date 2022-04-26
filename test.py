import unittest
import app

class MyTestCase(unittest.TestCase):
    def setUp(self):
        """
        Setting Up app for testing
        """
        app.connex_app.testing = True
        self.app = app.connex_app.app.test_client()
    
    def test_home(self):
        """
        Testing that Homepage is redirect to '/api/ui'
        """
        result = self.app.get('/')
        self.assertIn(b'target URL: <a href="/api/ui">/api/ui</a>',result.data, "wrong homepage result")
 
    
    def test_api_director(self):
        """
        Testing Director API for Read
        """
        result = self.app.get('/api/directors')
        self.assertEqual(result.status_code, 200, "something wrong with the Director API GET:/api/directors")

    def test_api_movie(self):
        """
        Testing Movie API for Read
        """
        result = self.app.get('/api/movies')
        self.assertEqual(result.status_code, 200, "something wrong with the Movie API GET:/api/movies")
       
if __name__ == '__main__':
    unittest.main()