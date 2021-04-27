from pathlib import Path

from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required
import pandas as pd
import matplotlib.pyplot as plt

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/', defaults={'name': 'Anonymous'})
@main_bp.route('/<name>')
def index(name):
    if not current_user.is_anonymous:
        name = current_user.firstname
    return render_template('index.html', title="Home page", name=name)


@main_bp.route('/mpl')
@login_required
def mpl():
    data_folder = Path('../data')
    Excel_file = 'international-visitors-london.xlsx'
    data = pd.read_excel(data_folder / Excel_file, sheet_name='Raw data')
    url = create_mpl_chart(data)

    return render_template('chart_mpl.html', url=url, url_=url,title="Pie chart")


def create_mpl_chart(data):
    y = data['mode'].values.tolist()
    a = y.count('Air')
    b = y.count('Sea')
    c = y.count('Tunnel')
    d = a + b + c
    x = [(a / d) * 100, (b / d) * 100, (c / d) * 100]
    label = ['Air', 'Sea', 'Tunnel']
    colors = ['skyblue', 'blue', 'gold']
    _explode = (0.1, 0, 0)

    Purpose = data['purpose'].values.tolist()
    A = Purpose.count('Holiday')
    B = Purpose.count('Business')
    C = Purpose.count('VFR')
    D = Purpose.count('Miscellaneous')
    F = Purpose.count('Study')
    E = A + B + C + D + F
    X = [(A / E) * 100, (B / E) * 100, (C / E) * 100, (D / E) * 100, (F / E) * 100]
    Labels = ['Holiday', 'Business', 'VFR', 'Miscellaneous', 'Study']
    _Explode = (0.1, 0.08, 0.09, 0.07, 0.06)

    fig, (ax1, ax2) = plt.subplots(2,1)

    ax1.pie(x, labels=label, autopct='%1.1f%%', colors=colors, explode=_explode, shadow=True)
    ax2.pie(X, labels=Labels, autopct='%1.2f%%', explode=_Explode, shadow=True)
    fig.tight_layout()
    url = 'static/img/plot.png'
    fig.savefig(url)
    return url


@main_bp.route('/dash_app1')
def dash_app1():
    return redirect('/dash_app1/')
