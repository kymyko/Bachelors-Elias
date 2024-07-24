from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models import Articles, Users, db, Psychologists
from app.forms import ArticleForm, WorkingHoursForm

import json

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    initial_question = "Hello! How can I assist you today?"
    # Query articles from the database
    articles = Articles.query.all()
    psychologists = Psychologists.query.all()
    return render_template('index.html', initial_question=initial_question, articles=articles,
                           psychologists=psychologists, is_main_page=True)



@bp.route('/psychologist/<int:id>/profile', methods=['GET'])
def psychologist_profile(id):
    psychologist = get_psychologist_by_id(id)
    if psychologist:
        working_hours = json.loads(psychologist.working_hours)

        # Assuming you have a WorkingHoursForm class defined in forms.py
        form = WorkingHoursForm()

        # Here, you need to define or retrieve the schedule variable
        schedule = get_schedule_for_psychologist(id)  # Example function to retrieve schedule

        return render_template('psychologist_profile.html', psychologist=psychologist, working_hours=working_hours,
                               form=form)
    else:
        flash("Psychologist not found", "error")
        return redirect(url_for('main.index'))


def get_schedule_for_psychologist(id):
    return Psychologists.query.get(id)


def get_psychologist_by_id(id):
    return Psychologists.query.get(id)


@bp.route('/article/<int:id>')
def show(id):
    article = Articles.query.get_or_404(id)
    author = Users.query.get(article.author_id)
    return render_template('show.html', article=article, author=author)


@bp.route('/article/create', methods=['GET', 'POST'])
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
    return render_template('create.html', form=form)


@bp.route('/article/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    article = Articles.query.get_or_404(id)
    if article.author_id != current_user.id:
        flash('You do not have permission to edit this article', 'danger')
        return redirect(url_for('main.index'))

    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        article.title = form.title.data
        article.description = form.description.data
        article.content = form.content.data
        db.session.commit()
        flash('Article updated successfully!', 'success')
        return redirect(url_for('main.show', id=article.id))
    return render_template('edit.html', form=form, article=article)
