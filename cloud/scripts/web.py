
# web.py

#- Imports -----------------------------------------------------------------------------------------

from flask    import Flask, request, render_template_string
from .control import mqtt_write1, mqtt_write2
from .system  import get_temperature

#- HTML Page----------------------------------------------------------------------------------------

app = Flask(__name__)

# Local variables to store the settings
settings = {
        'motor': '',
        'temperature_threshold': 0,
        'moisture_threshold': 0,
        'city': ''
        }

# HTML template for the form
form_template = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Settings</title>
    <style>
               body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px 30%;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        form {
            background: #fff;
            padding: 50px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"],
        input[type="number"] {
            width: 90%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"],
        button {
            background-color: #5cb85c;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover,
        button:hover {
            background-color: #4cae4c;
        }
        h2 {
            margin-top: 20px;
        }
    </style>
</head>

<body>
    <h1>Configure Variables</h1>
    <form method="POST">
        <label for="motor">Motor:</label>
        <button type="submit" name="toggle_motor" value="1">
            Toggle Motor
        </button>
        <br><br>

        <label for="temperature_threshold">Temperature Threshold:</label>
        <input type="number" id="temperature_threshold" name="temperature_threshold" value="{{ temperature_threshold }}">
        <br><br>

        <label for="moisture_threshold">Moisture Threshold:</label>
        <input type="number" id="moisture_threshold" name="moisture_threshold" value="{{ moisture_threshold }}">
        <br><br>

        <label for="city">City:</label>
        <input type="text" id="city" name="city" value="{{ city }}">
        <br><br>

        <input type="submit" value="Save Config">
    </form>
</body>
</html>
"""


#- App Main ----------------------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Update settings with form data
        if 'toggle_motor' in request.form:
                settings['motor'] = 'm'
        settings['temperature_threshold'] = request.form.get('temperature_threshold', type=int)
        settings['moisture_threshold'] = request.form.get('moisture_threshold', type=int)
        settings['city'] = request.form.get('city', '')

        # Set values
        mqtt_write1("motor", settings['motor'])
        mqtt_write1("temperature_threshold", settings['temperature_threshold'])
        mqtt_write2(settings['moisture_threshold'])
        get_temperature(settings['city'])

    return render_template_string(form_template, **settings)

def run_webserver():
    app.run()

