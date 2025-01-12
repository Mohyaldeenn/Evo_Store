from django.test import TestCase
from datetime import datetime
# Create your tests here.
order_id = datetime.today().strftime('%y%m%d')
print(order_id)