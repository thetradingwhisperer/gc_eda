import pandas as pd
import numpy as np

#defining the features
def candle_feat(data):
    """ 
        Function to calculate candle features
    """
    data['returnToday'] = data.Close - data.Open
    data['candleToday'] = [1 if var > 0 else -1 for var in data['returnToday']]

    # lagged candle features
    for i in range(1, 5):
      data['candle_lag_' + str(i)] = data.candleToday.shift(i)
      
    data['candleNextDay'] = data.candleToday.shift(-1)
    data['returnNextDay'] = data.returnToday.shift(-1)
  
    ### Final features
    # Create a new feature: 0 for bear candle, 1 for bull candle - for lag 3. e.g 000 for past 3 bear candle and 001 for past 2 bear candle and 1 bull candle in order
    data['historical_candle'] = data['candleToday'].astype(str) + data['candle_lag_2'].astype(str) + data['candle_lag_1'].astype(str)
    # bin return range into 4 groups
    data['returnGroup'] = pd.qcut(data['returnToday'], 4, labels=False)

    data.dropna(inplace=True)

    return data