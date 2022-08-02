from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np

class stlb:

    def __init__(
            self,
            train_X: np.array,
            train_y: np.array,
            test_X: np.array,
            shift = 'auto',
            period: int = 7,
            type = 'additive',
            extrapolate_trend='freq'
            ):
        self.train_X = train_X
        self.train_y = train_y
        self.test_X = test_X

        self.test_num = self.test_X.shape[0]

        if shift == 'auto':
            self.shift = self.test_num
        else:
            assert shift >= self.test_num
            self.shift = shift

        assert type in ['additive','multiplicative']

        self.period = period
        self.type = type
        self.extrapolate_trend = extrapolate_trend

    def fit(
        self
        ):
        X_shift = self.train_X[:-self.shift]
        y_shift = self.train_y[self.shift:]

        test_decomp = np.concatenate([self.train_X,self.test_X],axis=0)

        sd_train_X = seasonal_decompose(X_shift,period=self.period,model=self.type,extrapolate_trend=self.extrapolate_trend)
        sd_train_y = seasonal_decompose(y_shift,period=self.period,model=self.type,extrapolate_trend=self.extrapolate_trend)
        test_decomp = seasonal_decompose(test_decomp,period=self.period,model=self.type,extrapolate_trend=self.extrapolate_trend)

        rf = RandomForestRegressor()

        # trend
        rf.fit(sd_train_X.trend,sd_train_y.trend)
        self.trend = rf.predict(test_decomp.trend[-self.test_num:])

        # seasonal
        rf.fit(sd_train_X.seasonal,sd_train_y.seasonal)
        self.seasonal = rf.predict(test_decomp.seasonal[-self.test_num:])

        # resid
        rf.fit(sd_train_X.seasonal,sd_train_y.resid)
        self.resid = rf.predict(test_decomp.resid[-self.test_num:])
        
    def predict(
        self
        ):
        if self.type == 'additive':
            return self.trend + self.seasonal + self.resid
        if self.type == 'multiplicative':
            return self.trend * self.seasonal * self.resid