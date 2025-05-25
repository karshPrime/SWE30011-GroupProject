import serial
import time
from flask import Flask, render_template, request

app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600)

buzzer_threshold = 20

def read_soil_sensor():
    global buzzer_threshold
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("moisture:"):
            try:
                soil_moisture = int(line.split(":")[1])
                print(f"Soil moisture: {soil_moisture}%")
                
                if soil_moisture < buzzer_threshold:
                    ser.write(b"1\n")
                else:
                    ser.write(b"0\n")
            except ValueError:
                pass
            

@app.route('/', methods=['GET', 'POST'])
def index():
    global buzzer_threshold
    if request.method == 'POST':
        new_threshold = request.form.get('threshold')
        if new_threshold:
            try:
                buzzer_threshold = int(new_threshold)
                print(f"New buzzer threshold set: {buzzer_threshold}")
            except ValueError:
                pass

    templateData = {
        'buzzer threshold': buzzer_threshold
    }
    return render_template('index.html', **templateData)



if __name__ == '__main__':
    import threading
    
    def sensor_loop():
        while True:
            read_soil_sensor()
            time.sleep(0.2)
    
    thread = threading.Thread(target=sensor_loop)
    thread.daemon = True
    thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=8080)
