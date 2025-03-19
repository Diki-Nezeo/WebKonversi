from flask import Flask, render_template, request

app = Flask(__name__)

# Fungsi Konversi Satuan
def convert(value, from_unit, to_unit, category):
    conversions = {
        "suhu": {
            "celsius": {"fahrenheit": (value * 9/5) + 32, "kelvin": value + 273.15},
            "fahrenheit": {"celsius": (value - 32) * 5/9, "kelvin": ((value - 32) * 5/9) + 273.15},
            "kelvin": {"celsius": value - 273.15, "fahrenheit": ((value - 273.15) * 9/5) + 32},
        },
        "jarak": {
            "meter": {"kilometer": value / 1000, "mil": value * 0.000621371},
            "kilometer": {"meter": value * 1000, "mil": value * 0.621371},
            "mil": {"meter": value / 0.000621371, "kilometer": value / 0.621371},
        },
        "berat": {
            "kilogram": {"gram": value * 1000, "pon": value * 2.20462},
            "gram": {"kilogram": value / 1000, "pon": value * 0.00220462},
            "pon": {"kilogram": value / 2.20462, "gram": value / 0.00220462},
        }
    }

    return conversions.get(category, {}).get(from_unit, {}).get(to_unit, "Konversi tidak tersedia")

@app.route("/", methods=["GET", "POST"])
def index():
    hasil_suhu, hasil_jarak, hasil_berat = None, None, None

    if request.method == "POST":
        try:
            value = float(request.form["value"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]
            category = request.form["category"]

            hasil = convert(value, from_unit, to_unit, category)

            if category == "suhu":
                hasil_suhu = hasil
            elif category == "jarak":
                hasil_jarak = hasil
            elif category == "berat":
                hasil_berat = hasil

        except:
            if category == "suhu":
                hasil_suhu = "Input tidak valid"
            elif category == "jarak":
                hasil_jarak = "Input tidak valid"
            elif category == "berat":
                hasil_berat = "Input tidak valid"

    return render_template("index.html", hasil_suhu=hasil_suhu, hasil_jarak=hasil_jarak, hasil_berat=hasil_berat)

if __name__ == "__main__":
    app.run(debug=True)
