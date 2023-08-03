import pandas as pd
import numpy as np

#defining the features
def candle_feat(data):
    """ 
        Function to calculate candle features
    """
    
    data['maFast'] = data['Close'].ewm(span=7, adjust=False).mean()
    data['maFast_1'] = data['maFast'].shift(1)
    data['maSlow'] = data['Close'].ewm(span=21, adjust=False).mean()
    data['closeOverMaFast'] = ["1" if var > i else "0" for i, var in zip(data['Close'], data['maFast_1'])]
    data['closeOverMaSlow'] = ["1" if var > i else "0" for i, var in zip(data['Close'], data['maSlow'])]
    data['MaFastOverMaSlow'] = ["1" if var > i else "0" for i, var in zip(data['maFast'], data['maSlow'])]
    data['returnToday'] = data.Close - data.Open
    data['candleToday'] = ["1" if var > 0 else "0" for var in data['returnToday']]
    data['candleNow'] = [1 if var > 0 else 0 for var in data['returnToday']]

    # lagged candle features
    for i in range(1, 5):
      data['candle_lag_' + str(i)] = data.candleToday.shift(i)
      
    data['candleNextDay'] = data.candleNow.shift(-1)
    data['returnNextDay'] = data.returnToday.shift(-1)
    returnRange = abs(data['returnNextDay'])
  
    ### Final features
    # Create a new feature: 0 for bear candle, 1 for bull candle - for lag 3. e.g 000 for past 3 bear candle and 001 for past 2 bear candle and 1 bull candle in order
    data['historical_candle_2'] = data['candleToday'].astype(str) + data['candle_lag_1'].astype(str) + '--' + data['closeOverMaFast'].astype(str) + data['closeOverMaSlow'].astype(str)
    data['historical_candle_3'] = data['candleToday'].astype(str) + data['candle_lag_1'].astype(str) + data['candle_lag_2'].astype(str) + '--' + data['closeOverMaFast'].astype(str) + data['closeOverMaSlow'].astype(str)
    # bin return range into 4 groups
    data['returnGroup'] = pd.qcut(returnRange, 4, labels=False)

    data.dropna(inplace=True)

    return data