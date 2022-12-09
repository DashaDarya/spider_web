from work_with_redis import WorkWithRedis
from flask import Flask, render_template, request, redirect, url_for
import json
from get_text_to_good_fit import TextGoodFit

app = Flask(__name__)



@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        phrase_to_search = request.form["phrase"]
        return redirect(url_for("response", search_phrase=phrase_to_search))
    else:
        return render_template("index.html")

@app.route('/responses/<search_phrase>', methods=["GET"])
def response(search_phrase: str):
    answer = WorkWithRedis.get_resources(search_phrase)
    # функция красоты
    answer, number = TextGoodFit.get_text_to_good_fit(answer)

    

    return render_template("response.html", number=number, answer=answer)

if __name__=="__main__":
    app.run(debug=True)

# PHRASE_TO_SEARCH = 'Москвич 3' 