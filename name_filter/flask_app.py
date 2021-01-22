from flask import Flask, render_template, request
import name_filter
nameFilter = name_filter.NameFilter(interactive_add=False, interactive_adapt=False)
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def init():

    if request.method == 'POST':
        result = nameFilter.classify(request.form['text'], True)
        threshold = float(request.form['threshold'])
        rating = result['rating']
        if rating >= threshold:
            name_text = f'{len(result["candidates"])} names found! </br>' + request.form['text']
            for candidate in result['candidates']:
                name_text = name_text.replace(candidate, f'<font color="red">{candidate}</font>')
        else:
            name_text = 'No names found! </br>' + request.form['text']
    else:
        name_text = None
        rating = None
        threshold = None
    return render_template("name_test.html", name_text=name_text, threshold=threshold, rating=rating)
