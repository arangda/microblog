from flask import render_template
from app.shares import bp
from flask_login import login_required
from app.shares.forms import ShareForm

@bp.route('/gupiao')
@login_required
def gupiao():
    return render_template('share/index_share.html')


@bp.route('/addshare')
@login_required
def add_share():
    form = ShareForm()
    return render_template('share/add_share.html',form=form)