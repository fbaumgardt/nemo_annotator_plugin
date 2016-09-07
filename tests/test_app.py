from unittest import TestCase
from nemo_plokamos_plugin import PlokamosPlugin
import os


class TestPlugin(TestCase):
    def setUp(self):

        self.query1 = open(os.path.join(os.path.dirname(__file__),'test_data','query1.json')).read()
        self.query1_user = { 'uri':  "http://data.perseus.org/sosol/users/John%20Shepard,%20Joseph%20Caplan,%20Luke%20O'Connor" ,
                             'name': "Perseids User"}
        self.bad_user = {'uri': "http://data.perseus.org/sosol/users/abc", 'name':'abc user'}
        self.plugin = PlokamosPlugin(annotation_select_endpoint="http://example.org", annotation_update_endpoint="http://example.org")

    def test_is_authorized(self):
        assert self.plugin.is_authorized(query=self.query1,user_uri=self.query1_user['uri'])
        assert not self.plugin.is_authorized(query=self.query1,user_uri=self.bad_user['uri'])


