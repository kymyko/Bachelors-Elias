from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Articles, db, Users
from app.forms import ArticleForm

bp = Blueprint('articles', __name__, url_prefix='/articles')


@bp.route('/')
def index():
    articles = Articles.query.all()
    return render_template('main.index', articles=articles)


@bp.route('/article/<int:id>', methods=['GET'])
def detail(id):
    article = Articles.query.get_or_404(id)
    author = Users.query.get(article.author_id)
    return render_template('show.html', article=article)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Articles(
            title=form.title.data,
            description=form.description.data,
            content=form.content.data,
            author_id=current_user.id
        )
        db.session.add(new_article)
        db.session.commit()
        flash('Article created successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('articles/create.html', form=form)


@bp.route('/article/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    article = Articles.query.get_or_404(id)
    if article.author_id != current_user.id:
        flash('You do not have permission to edit this article', 'error')
        return redirect(url_for('main.index'))

    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        article.title = form.title.data
        article.description = form.description.data
        article.content = form.content.data
        db.session.commit()
        flash('Article updated successfully!', 'success')
        return redirect(url_for('articles.detail', id=article.id))
    return render_template('articles/edit.html', form=form, article=article)


@bp.route('/article/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    article = Articles.query.get_or_404(id)
    if article.author_id == current_user.id or current_user.id == 3:
        db.session.delete(article)
        db.session.commit()
        flash('Article deleted successfully!', 'success')
    else:
        flash('You do not have permission to delete this article.', 'error')
    return redirect(url_for('users.profile'))

