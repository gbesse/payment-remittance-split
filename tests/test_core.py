import unittest,copy,json
from payment_remittance_split import run
DEMO={'currency': 'EUR', 'invoices': [{'id': 'i1', 'amount': '60.00'}, {'id': 'i2', 'amount': '40.00'}], 'payments': [{'id': 'p', 'amount': '90.00'}], 'allocations': [{'invoice': 'i1', 'payment': 'p', 'amount': '60.00'}, {'invoice': 'i2', 'payment': 'p', 'amount': '30.00'}]}
class DomainTests(unittest.TestCase):
 def test_split_and_residual(self):
  x=run(DEMO);self.assertTrue(x['valid']);self.assertEqual(x['invoices'][1]['remaining'],'10.00');self.assertEqual(x['payments'][0]['unallocated'],'0.00')
 def test_overallocated_payment_detected(self):
  x=copy.deepcopy(DEMO);x['allocations'][1]['amount']='40.00';y=run(x);self.assertFalse(y['valid']);self.assertTrue(y['payments'][0]['overallocated'])
 def test_duplicate_pair_not_double_counted(self):
  x=copy.deepcopy(DEMO);x['allocations'].append(x['allocations'][0])
  with self.assertRaises(ValueError):run(x)
