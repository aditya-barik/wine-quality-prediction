from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
import os

from wine_quality_prediction_service import wine_quality_prediction


webapp_root = "wine_quality_prediction_app"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        try:
            if request.form:
                data_request = dict(request.form)
                prediction = wine_quality_prediction.get_web_response(
                    data_request
                )
                return render_template("index.html", response=prediction)
            elif request.json:
                response = wine_quality_prediction.get_api_response(
                    request.json
                )
                return jsonify(response)
            pass

        except Exception as e:
            error = {"error": e}
            return render_template("404.html", error=error)
        pass
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
