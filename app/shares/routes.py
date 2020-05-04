from app import db
from flask import render_template,flash,request,redirect,url_for
from app.shares import bp
from flask_login import login_required
from app.shares.forms import ShareForm,CategoryForm,TagForm
from app.shares.models import Share,Category,Tag
from app.shares.utils import slugify,marktohtml,flash_errors

@bp.route('/gupiao')
@login_required
def index():
    page = request.args.get('page',1,type=int)
    pagination = Share.query.order_by(Share.id.desc()).paginate(
        page,per_page=50
    )
    shares = pagination.items
    return render_template('share/index_share.html',page=page,pagination=pagination,shares=shares)

@bp.route('/share/search')
@login_required
def share_search():
    q = request.args.get('q','').strip()
    if q=='':
        flash('请输入搜索内容','warning')
        return redirect_back()
    page = request.args.get('page',1,type=int)
    per_page = 50
    pagination = Share.query.whooshee_search(q).paginate(page,per_page)
    shares = pagination.items
    return render_template('manage_share.html',page=page,ahares=shares,pagination=pagination)


@bp.route('/addshare',methods=['GET','POST'])
@login_required
def add_share():
    form = ShareForm()
    if form.validate_on_submit():
        markdown_con = form.markdown.data
        intro = marktohtml(form.markdown.data)
        share = Share(
            name=form.name.data,\
            code=form.code.data,\
            intro=intro,\
            markdown=markdown_con,\
            category_id=form.category.data
        )
        db.session.add(share)
        db.session.commit()
        flash('股票添加成功')
    return render_template('share/add_share.html',form=form)

@bp.route("/share/<int:share_id>/update", methods=['GET', 'POST'])
@login_required
def update_share(share_id):
    share = Share.query.get_or_404(share_id)
    form = ShareForm()
    if form.validate_on_submit():
        share.name = form.name.data
        share.code = form.code.data
        share.category_id = form.category.data
        share.markdown = form.markdown.data
        share.intro = marktohtml(form.markdown.data)
        db.session.commit()
        flash('股票已更新!', 'success')
        return redirect(url_for('shares.show_share',share_id=share.id))
    elif request.method == 'GET':
        form.name.data = share.name
        form.code.data = share.code
        form.category.data = share.category_id
        form.markdown.data = share.markdown
    return render_template('share/add_share.html', title='更新文章',
                        form=form, legend='更新')



@bp.route("/share/<int:share_id>/delete", methods=['POST'])
@login_required
def delete_share(share_id):
    share = Share.query.get_or_404(share_id)
    db.session.delete(share)
    db.session.commit()
    flash('Your share has been deleted!', 'success')
    return redirect(url_for('shares.index'))


@bp.route('/<int:share_id>',methods=['GET','POST'])
def show_share(share_id):
    share = Share.query.filter_by(id=share_id).first_or_404()

    share.views = share.views + 1  
    tag_form = TagForm()
    return render_template('share/show_share.html',share=share,tag_form=tag_form)

@bp.route('/n/<int:share_id>')
def share_next(share_id):
    share = Share.query.get_or_404(share_id)
    share_n = Share.query.filter(Share.id < share_id).order_by(Share.id.desc()).first()
    if share_n is None:
        flash('已经是最后了','info')
        return redirect(url_for('.show_share',share_id=share_id))
    return redirect(url_for('.show_share',share_id=share_n.id))

@bp.route('/p/<int:share_id>')
def share_previous(share_id):
    share = Share.query.get_or_404(share_id)
    share_p = Share.query.filter(Share.id > share_id).order_by(Share.id.asc()).first()
    if share_p is None:
        flash('已经是最前了','info')
        return redirect(url_for('.show_share',share_id=share_id))
    return redirect(url_for('.show_share',share_id=share_p.id))

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
    page = request.args.get('page',1,type=int)
    pagination = Category.query.order_by(Category.id.desc()).paginate(
        page,per_page=20
    )
    categories = pagination.items
    return render_template('share/manage_category.html',page=page,pagination=pagination,categories=categories)



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
    return render_template('share/edit_category.html',form=form)

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
    per_page = current_app.config['FLASKBLOG_MANAGE_share_PER_PAGE']
    agination = Share.query.with_parent(category).order_by(Share.date_shareed.desc())\
                     .paginate(page,per_page)
    shares = pagination.items
    return render_template('home.html',subtitle='分类:'+category.name,pagination=pagination,shares=shares)


@bp.route('/tag-<string:english_name>')
def show_tag(english_name):
    tag = Tag.query.filter_by(english_name=english_name).first_or_404()
    page = request.args.get('page',1,type=int)
    per_page = 50
    pagination = Share.query.with_parent(tag).order_by(Share.id.desc()).paginate(page,per_page)
    shares = pagination.items

    return render_template('home.html',subtitle='标签:'+tag.name,pagination=pagination,shares=shares)


@bp.route('/share/<int:share_id>/tag/new',methods=['POST'])
@login_required
def new_tag(share_id):
    share = Share.query.get_or_404(share_id)
    form = TagForm()
    if form.validate_on_submit():
        for name in form.tag.data.split("#"):   #以"#"好分隔tag
            lname = name.lower()
            tag = Tag.query.filter_by(name=lname).first()
            if tag is None:
                tag = Tag(name=lname,english_name=slugify(lname))
                db.session.add(tag)
                db.session.commit()
            if tag not in share.tags:
                share.tags.append(tag)
                db.session.commit()
        flash('Tag 添加成功','success')
    
    flash_errors(form)
    return redirect(url_for('.show_share',share_id=share.id))


@bp.route('/delete/tag/<int:share_id>/<int:tag_id>',methods=['POST'])
@login_required
def delete_tag(share_id,tag_id):
    share = Share.query.get_or_404(share_id)
    tag = Tag.query.get_or_404(tag_id)
    share.tags.remove(tag)
    db.session.commit()

    if not tag.shares:
        db.session.delete(tag)
        db.session.commit()

    flash('标签已删除。','info')
    return redirect(url_for('.show_share',share_id=share.id))
