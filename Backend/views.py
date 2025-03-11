from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
import os

views = Blueprint('views', __name__, template_folder=os.path.abspath("./Frontend/templates"))

@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():
  print('Debug: runs view.home')
  return render_template("index.html", user=current_user)