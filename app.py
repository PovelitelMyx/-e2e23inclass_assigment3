from flask import Flask, request
import joblib
import numpy
from sklearn.tree import DecisionTreeRegressor

MODEL_PATH = 'mlmodels/model_DecisionTreeRegressor2.pkl'
SCALER_X_PATH = 'mlmodels/scaler_standard_x.pkl'
SCALER_Y_PATH = 'mlmodels/scaler_standard_y.pkl'

app = Flask(__name__)
model = joblib.load(MODEL_PATH)
sc_x = joblib.load(SCALER_X_PATH)
sc_y = joblib.load(SCALER_Y_PATH)


@app.route('/predict_price', methods=['GET'])
def predict():  # put application's code here
    args = request.args
    open_plan = args.get('open_plan', default=-1, type=int)
    rooms = args.get('rooms', default=-1, type=int)
    area = args.get('area', default=-1, type=float)
    renovation = args.get('renovation', default=-1, type=int)

    x = numpy.array([open_plan, rooms, area, renovation]).reshape(1, -1)
    x = sc_x.transform(x)
    result = model.predict(x)
    result = sc_y.inverse_transform(result.reshape(1, -1))

    return str(result[0][0])


if __name__ == '__main__':
    app.run(debug=True, port=5444, host='0.0.0.0')
