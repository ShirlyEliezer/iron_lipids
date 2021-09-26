from processor import *
from predictor import *


def categorical_cross_val(data):
    """
    This function performs cross validation using 'leave one out' method.
    The function predicts the target variable using one or several predictors.
    """
    # create our independent variables
    X = data[[IRON, IRON_TYPE, LIPID, LIPID_TYPE]]
    # get numeric representation of lipid types
    X = pd.get_dummies(data=X, drop_first=False)

    for col in X.columns[2:5]:
        X[col] = X[col] * X[IRON]
    for col in X.columns[5:8]:
        X[col] = X[col] * X[LIPID]
    y = np.array(data[R1])
    X = np.array(X[X.columns[2:]]).reshape(-1, 6)

    # normalize the data
    for i in range(len(X[0])):
        X[:, i] = scale(X[:, i])

    pred = Predictor(X, y, data)
    pred.plot()


def cross_val(data):
    models = {
            'IRON': np.array(data[IRON]).reshape(-1, 1),
            'LIPID': np.array(data[LIPID]).reshape(-1, 1),
            'IRON, LIPID': np.array(data[[IRON, LIPID]]).reshape(-1, 2),
            'IRON, LIPID, IRON * LIPID': np.hstack((np.array(data[[IRON, LIPID]]).reshape(-1, 2),
                                                    np.array(data[IRON] * data[LIPID]).reshape(
                                                        -1, 1))),
            'IRON * LIPID': np.array(data[IRON] * data[LIPID]).reshape(-1, 1),
    }

    for model in models:
        # create X, y
        X = models[model]
        y = np.array(data[R1])
        # normalize the data
        for i in range(len(X[0])):
            X[:, i] = scale(X[:, i])

        pred = Predictor(X, y, data)
        pred.plot()


if __name__ == '__main__':

    pro = Processor()
    pro.pre_processing()
    pro.detect_outliers()
    pro.relations_target(IRON_TYPE, R1, IRON)
    pro.relations_target(LIPID_TYPE, R1, LIPID)
    cross_val(pro.get_data())
    categorical_cross_val(pro.get_data())