from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__,)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method=='POST':
        note = request.form.get('note')

        if len(note)<1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added', category='success')

    return render_template("home.html", user=current_user)


@views.route('delete-note/<note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Note Deleted', category="success")   
    return redirect(url_for("views.home"))
    