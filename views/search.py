import requests
from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress, Length

search_bp = Blueprint("search", __name__)


class ZipCodeForm(FlaskForm):
    zipCode = StringField(
        label="Digite o CEP:", validators=[DataRequired(), Length(min=8), Length(max=8)]
    )
    submit = SubmitField("Buscar", name="submit-zip-code")


class LocationForm(FlaskForm):
    location = StringField(
        label="Digite o IP:",
        validators=[IPAddress(), DataRequired(), Length(min=7), Length(max=39)],
    )
    submit = SubmitField("Buscar", name="submit-location")


def get_form_kwargs(form1, form2):
    return {"zipCodeForm": form1, "locationForm": form2}


@search_bp.route("/busca", methods=["GET", "POST"])
def search():
    zipCodeForm = ZipCodeForm()
    locationForm = LocationForm()
    zipCodeData = None
    zipCodeMessage = None
    locationMessage = None
    locationData = None

    if request.method == "POST":
        if "submit-zip-code" in request.form:
            zipCode = zipCodeForm.zipCode.data

            try:
                response = requests.get(f"https://viacep.com.br/ws/{zipCode}/json")
                zipCodeData = response.json()

                if zipCodeData.get("erro"):
                    zipCodeMessage = "CEP inválido, por favor digite outro valor"

            except:
                zipCodeMessage = "CEP inválido, por favor digite outro valor"

        elif "submit-location" in request.form:
            location = locationForm.location.data

            try:
                response = requests.get(f"https://ipapi.co/{location}/json/")
                locationData = response.json()

                if locationData.get("error"):
                    if locationData.get("reason") == "RateLimited":
                        locationMessage = (
                            "Consulte o IP mais tarde, as consultas foram excedidas"
                        )
                    else:
                        locationMessage = "IP inválido, por favor digite outro valor"
                    locationData = None

            except:
                locationMessage = "Erro inesperado, volte a se consultar mais tarde"

    return render_template(
        "search.html",
        zipCodeForm=zipCodeForm,
        locationForm=locationForm,
        zipCodeData=zipCodeData,
        zipCodeMessage=zipCodeMessage,
        locationData=locationData,
        locationMessage=locationMessage,
    )
