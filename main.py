from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Access data from file
stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


# Create a home page
@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


# Create end point using station and date
@app.route("//api/v1/<station>/<date>/")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}


# Create end point using station
@app.route("/api/v1/<station>/")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    results = df.to_dict(orient="records")
    return results


# Create end point using station and year
@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    results = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return results


app.run(debug=True)
