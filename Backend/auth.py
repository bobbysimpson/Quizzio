from flask import Blueprint, render_template, request, flash, jsonify, url_for
import os


auth = Blueprint('auth', __name__, template_folder=os.path.abspath("./Frontend/templates"))

@auth.route('/', methods=['GET', 'POST'])
def home():
  return render_template('login.html')