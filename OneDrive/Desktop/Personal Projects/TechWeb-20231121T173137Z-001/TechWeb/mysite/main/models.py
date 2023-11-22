from django.db import models
from ConnectingToAVAPI import Data
 # Create your models here.
class GraphData(models.Model):
    date = models.DateField()
    value = models.FloatField()

    @classmethod
    def fetch_and_store_data(cls, four_or_three, ticker, indicator_type, window):
        # Use the Data class from connectingtoAVAPI to fetch data
        c_object = Data(ticker)

        if four_or_three not in ('four', 'three'):
            raise ValueError("four_or_three must be either 'four' or 'three'")
        else:
            if four_or_three == 'four':
                indicator_data = c_object.four_type_indicator(indicator_type, window)
            else:
                indicator_data = c_object.three_type_indicator(indicator_type, window)


        # ... Add other indicators

        # Store the fetched data in the database
        for date, value in indicator_data.items():
            cls.objects.create(date=date, value=value)
