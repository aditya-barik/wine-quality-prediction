from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
import joblib
import os

import numpy as np
# from wine_quality_prediction_service import wine_quality_prediction

from src.utils import load_config

webapp_root = "wine_quality_prediction_app"
config_path = "params.yaml"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


def predict(data):
    config = load_config(config_path=config_path)
    model = joblib.load(
        os.path.join(config["web_app_model_dir"], "model.joblib")
    )
    prediction = model.predict(data)[0]
    print("prediction : ", prediction)
    return prediction


def api_response(request):
    try:
        data = np.array([list(request.json.values())])      # type: ignore
        prediction = predict(data)
        response = {"response": prediction}
        return response
    except Exception as e:
        print(e)
        error = {"error": "Something went wrong!! Try again later!"}
        return render_template("404.html", error=error)


@app.route("/", methods=["GET", "POST"])        # type: ignore
def index():

    if request.method == "POST":
        try:
            if request.form:
                data = [list(map(float, dict(request.form).values()))]
                prediction = predict(data)
                return render_template("index.html", response=prediction)
                # dict_req = dict(request.form)
                # response = prediction.form_response(dict_req)
                # return render_template("index.html", response=response)
            elif request.json:
                response = api_response(request)
                return jsonify(response)
            pass

        except Exception as e:
            print(e)
            error = {"error": "Something went wrong!! Try again later!"}
            # error = {"error": e}

            return render_template("404.html", error=error)
        pass
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
