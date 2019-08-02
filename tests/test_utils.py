import unittest
from mock import patch, Mock
import json

from grlc.fileLoaders import LocalLoader
import grlc.utils as utils

from tests.mock_data import mock_simpleSparqlResponse

class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.loader = LocalLoader('./tests/repo/')

    @patch('requests.get')
    def test_sparql_transformer(self, mock_get):
        mock_json = {
            "head": {},
            "results": {
                "bindings": [
                    {
                        "id": {
                            "type": "uri",
                            "value": "http://www.w3.org/2001/XMLSchema#anyURI"
                        },
                        "class": {
                            "type": "uri",
                            "value": "http://www.w3.org/2000/01/rdf-schema#Datatype"
                        },
                        "v2": {
                            "type": "literal",
                            "xml:lang": "en",
                            "value": "xsd:anyURI"
                        }
                    },
                    {
                        "id": {
                            "type": "uri",
                            "value": "http://www.w3.org/2001/XMLSchema#boolean"
                        },
                        "class": {
                            "type": "uri",
                            "value": "http://www.w3.org/2000/01/rdf-schema#Datatype"
                        },
                        "v2": {
                            "type": "literal",
                            "xml:lang": "en",
                            "value": "xsd:boolean"
                        }
                    }]
            }
        }

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.headers = {'Content-Type': 'application/json'}
        mock_get.return_value.text = json.dumps(mock_json)

        rq, _ = self.loader.getTextForName('test-json')

        self.assertIn('proto', rq)

        resp, status, headers = utils.dispatchSPARQLQuery(rq, self.loader, content=None, requestArgs={},
                                                          acceptHeader='application/json',
                                                          requestUrl='http://mock-endpoint/sparql', formData={})
        self.assertEqual(status, 200)
        self.assertIsInstance(resp, list)
        self.assertIn('http', resp[0]['id'])

    @patch('requests.get')
    def test_projection(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.headers = {'Content-Type': 'application/json'}
        mock_get.return_value.text = json.dumps(mock_simpleSparqlResponse)

        rq, _ = self.loader.getTextForName('test-projection')
        resp, status, headers = utils.dispatchSPARQLQuery(rq, self.loader, content=None, requestArgs={'id': 'http://dbpedia.org/resource/Frida_Kahlo'},
                                                          acceptHeader='application/json',
                                                          requestUrl='http://mock-endpoint/sparql', formData={})

        self.assertIsInstance(resp, list, 'Response should be a list')
        self.assertEqual(len(resp), 5, 'Response should have 5 entries')
        for item in resp:
            self.assertTrue('key' in item, 'Response items should contain a key')
            self.assertTrue('value' in item, 'Response items should contain a value')
        keys = [ item['key'] for item in resp ]
        values = [ item['value'] for item in resp ]

        self.assertTrue(all(k in keys for k in ['p1', 'p2', 'p3', 'p4', 'p5']), 'Response should contain all known keys')
        self.assertTrue(all(v in values for v in ['o1', 'o2', 'o3', 'o4', 'o5']), 'Response should contain all known values')
