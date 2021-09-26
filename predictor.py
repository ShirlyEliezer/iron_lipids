from plots import *


class Predictor:

    def __init__(self, X, y, data):
        """ initiate the Predictor instance """
        # build linear regression model
        self.model = LinearRegression()
        # define cross-validation method to use
        self.cross_validation = LeaveOneOut()
        self.X = X
        self.y = y
        self.mae = 0
        self.accuracy = 0
        self.data = data

    def scores(self):
        """ the function calculates the scores of the model after cross validation"""
        scores = cross_val_score(self.model, self.X, self.y, scoring='neg_mean_squared_error',
                                 cv=self.cross_validation, n_jobs=-1)
        self.accuracy = r2_score(self.y, self.predict())
        self.mae = mean(absolute(scores))

    def predict(self):
        """ the function returns predictions of the target based on cross validation linear
        regression"""
        return cross_val_predict(self.model, self.X, self.y, cv=self.cross_validation)

    def plot(self):
        """ the function create instance of Plot class and plots the data """
        self.scores()
        title = "R^2: " + str(float("{:.3f}".format(self.accuracy))) + " Mean absolute squared " \
                "error: " + str(float("{:.3f}".format(self.mae)))

        pl = Plots(self.y, self.predict(), "R1[1/sec] measured", "R1[1/sec] predicted", title, self.data)
        pl.plot()
