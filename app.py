from decimal import Decimal
from enum import Enum
from flask import Flask, flash, redirect, render_template, request, url_for

from wtforms import (
    Form,
    StringField,
    SelectField,
    DecimalField,
    DecimalRangeField,
)
from wtforms.widgets import RangeInput
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Email,
    AnyOf,
    EqualTo,
)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


class AutoModel(Enum):
    BMW = "BMW"
    AUDI = "Audi"
    NISSAN = "Nissan"


class Car(Form):
    name: str = StringField(validators=[DataRequired("WHERE ARE NAME??HUH??")])
    model: str = SelectField(
        choices=AutoModel.__members__,
        validators=[DataRequired(), AnyOf(AutoModel.__members__)],
    )
    price: Decimal = DecimalRangeField(
        widget=RangeInput(step=Decimal("0.1")),
        validators=[
            EqualTo("price_confirm"),
        ],
    )
    price_confirm: Decimal = DecimalRangeField(
        widget=RangeInput(step=Decimal("0.1")),
    )

    def save(self):
        print(f"name: {self.name}; model: {self.model}; price: {self.price}")


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/create")
def get_create():
    form = Car()

    return render_template("form.html", form=form)


@app.post("/edit")
def post_edit():
    car = Car()  # TODO : Get item from db
    form = Car(
        request.form,
    )
    if form.validate():
        form.populate_obj(car)
        car.save()
        return redirect(url_for(index.__name__))
    elif form.errors:
        print(f"{form.errors=}")
        print(f"{form.form_errors=}")
        for _, error in form.errors.items():
            flash(error)
    return render_template("form.html", form=form)


@app.post("/create")
def post_create():
    form = Car(
        request.form,
    )

    if form.validate():
        form.save()
        return redirect(url_for(index.__name__))
    elif form.errors:
        print(f"{form.errors=}")
        print(f"{form.form_errors=}")
        for _, error in form.errors.items():
            flash(error)
    return render_template("form.html", form=form)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
