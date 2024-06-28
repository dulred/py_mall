
from flask import render_template

from app.views.payforme import bp


@bp.route("/payforme",methods=["GET"])
def payforme():
	return render_template("payforme.html")