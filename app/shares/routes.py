from app import db
from flask import render_template,flash
from app.shares import bp
from flask_login import login_required
from app.shares.forms import ShareForm,CategoryForm
from app.shares.models import Share,Category
from app.shares.utils import slugify

@bp.route('/gupiao')
@login_required
def gupiao():
    return render_template('share/index_share.html')


@bp.route('/addshare',methods=['GET','POST'])
@login_required
def add_share():
    form = ShareForm()
    if form.validate_on_submit():
        share = Share(code=form.code.data)
        db.session.add(share)
        db.session.commit()
        flash(_('股票添加成功'))
    return render_template('share/add_share.html',form=form)


@bp.route('/category/new',methods=['GET','POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        if form.english_name.data:
            english_name = form.english_name.data
        else:
            english_name = slugify(form.name.data)
        category = Category(name=name,english_name=english_name)
        db.session.add(category)
        db.session.commit()
        flash('栏目已添加','success')
        return redirect(url_for('.manage_category'))
    return render_template('share/new_category.html',form=form)

@bp.route('/category/manage')
@login_required
def manage_category():
    categories = Category.query.order_by(Category.name).all()
    return render_template('share/manage_category.html',categories=categories)



@bp.route('/category/<int:category_id>/edit',methods=['GET','POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('不能编辑默认栏目','warning')
        return redirect(url_for('blog.index'))
    if form.validate_on_submit():
        category.name = form.name.data
        category.english_name = form.english_name.data
        db.session.commit()
        flash('已经修改','success')
        return redirect(url_for('.manage_category'))

    form.name.data = category.name
    form.english_name.data = category.english_name
    return render_template('edit_category.html',form=form)

@bp.route('/category/<int:category_id>/delete',methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('不能删除默认栏目','warning')
        return redirect(url_for('.manage_category'))
    category.delete()
    flash('栏目已删除','success')
    return redirect(url_for('.manage_category'))

@bp.route('/<string:category_name>')
def show_category(category_name,year=None):
    category = Category.query.filter_by(english_name=category_name,).first_or_404()
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['FLASKBLOG_MANAGE_POST_PER_PAGE']
    agination = Share.query.with_parent(category).order_by(Share.date_posted.desc())\
                     .paginate(page,per_page)
    shares = pagination.items
    return render_template('home.html',subtitle='分类:'+category.name,pagination=pagination,shares=shares)

