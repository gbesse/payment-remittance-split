from decimal import Decimal,InvalidOperation,ROUND_HALF_UP,localcontext
from .common import identifier,unique_ids,integer
def decimal(x):
 if not isinstance(x,str)or len(x)>80:raise ValueError('decimal_string')
 try:v=Decimal(x)
 except InvalidOperation as e:raise ValueError('decimal')from e
 if not v.is_finite()or abs(v)>Decimal('1e12'):raise ValueError('decimal_range')
 return v
def money(x):
 v=decimal(x)
 if v<0 or v!=v.quantize(Decimal('.01')):raise ValueError('minor_unit')
 return v
def run(data):
 invoices=data['invoices'];payments=data['payments'];allocations=data['allocations']
 if max(len(invoices),len(payments),len(allocations))>10000:raise ValueError('size')
 unique_ids(invoices);unique_ids(payments);currency=identifier(data['currency']);ib={r['id']:money(r['amount'])for r in invoices};pb={r['id']:money(r['amount'])for r in payments};isum={k:Decimal(0)for k in ib};psum={k:Decimal(0)for k in pb};seen=set()
 for a in allocations:
  i=identifier(a['invoice']);p=identifier(a['payment']);value=money(a['amount'])
  if i not in ib or p not in pb or(i,p)in seen:raise ValueError('unknown_or_duplicate_allocation')
  seen.add((i,p));isum[i]+=value;psum[p]+=value
 return {'currency':currency,'invoices':[{'id':k,'remaining':str((ib[k]-isum[k]).quantize(Decimal('.01'))),'overallocated':isum[k]>ib[k]}for k in ib],'payments':[{'id':k,'unallocated':str((pb[k]-psum[k]).quantize(Decimal('.01'))),'overallocated':psum[k]>pb[k]}for k in pb],'valid':all(isum[k]<=ib[k]for k in ib)and all(psum[k]<=pb[k]for k in pb),'money_moved':False}
