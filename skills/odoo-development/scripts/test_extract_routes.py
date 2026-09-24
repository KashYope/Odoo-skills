"""Regression tests for metadata extraction, not for a running Odoo server."""
import tempfile
import unittest
from pathlib import Path
from extract_routes import extract

class ExtractionTests(unittest.TestCase):
    def run_extract(self, source):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);p=root/'addons/example/controllers/main.py'
            p.parent.mkdir(parents=True);p.write_text(source)
            return extract(root,'19.0','example-sha')

    def test_metadata_and_empty_republication(self):
        rows,errors=self.run_extract('''from odoo import http
class Base(http.Controller):
 @http.route(['/one','/two'], type='http', auth='user', methods=['POST'])
 def operation(self, record_id, **kw):
  return request.env['sale.order'].browse(record_id).name
class Extension(Base):
 @http.route()
 def operation(self, *args, **kw):
  return super().operation(*args, **kw)
''')
        self.assertFalse(errors)
        self.assertEqual(rows[0]['routes_declared'],['/one','/two'])
        self.assertEqual(rows[0]['literal_models'],['sale.order'])
        self.assertNotIn('csrf',rows[0]['routing_declared'])
        self.assertEqual(rows[1]['routes_declared'],[])
        self.assertEqual(rows[1]['routing_declared'],{})
        self.assertIn('UNRESOLVED',rows[1]['effective_routing'])

    def test_import_alias_and_dynamic_path(self):
        rows,errors=self.run_extract('''from odoo.http import route as exposed
class C:
 @exposed(PATH, auth='public', readonly=lambda r,a: True)
 def route_method(self, **kw):
  return {'ok': True}
''')
        self.assertFalse(errors)
        self.assertEqual(rows[0]['routes_declared'],[{'expression':'PATH'}])
        self.assertIsInstance(rows[0]['routing_declared']['readonly'],dict)

    def test_syntax_error_is_reported(self):
        rows,errors=self.run_extract('@route(\ninvalid python')
        self.assertEqual(rows,[])
        self.assertEqual(len(errors),1)

if __name__=='__main__': unittest.main()
