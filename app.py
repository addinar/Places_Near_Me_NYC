from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index(): #defines a route for handling form submissions and displaying the result
    places_near_me = []
    if request.method == 'POST':
        user_zip = request.form['user_zip']
        places_url = "https://data.cityofnewyork.us/api/views/ssdk-4qjy/rows.json?accessType=DOWNLOAD"
        response = requests.get(places_url)
        places = response.json()

        zip_codes_url = "https://data.cityofnewyork.us/resource/pri4-ifjk.json"
        response = requests.get(zip_codes_url)
        zif = response.json()

        data = places["data"]

        for zip_code_info in zif:
            zip_code = zip_code_info["modzcta"]
            within = zip_code_info["label"]
            coordinates = zip_code_info['the_geom']['coordinates'][0][0]
            if str(user_zip) == zip_code or str(user_zip) in within:
                # print(zip_code)
                for area in data:
                    point = area[8]
                    _, lon_str, lat_str = point.split()
                    longitude = lon_str[1:6]
                    latitude = lat_str[0:5]
                    for coordinate in coordinates:
                        lon = str(coordinate[0])
                        lat = str(coordinate[1])
                        if longitude in lon and latitude in lat:
                            name = area[11]
                            if name not in places_near_me:
                                places_near_me.append(name)

    return render_template('index.html', places_near_me=places_near_me)

if __name__ == '__main__':
    app.run(debug=True)

