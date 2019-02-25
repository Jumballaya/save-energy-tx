'''
User Routes

These are the general routes for the user
'''
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
import stripe
from app.models.user import User
from app.user import bp
from app.user.forms import EditProfileForm
from app import db


# Set user last seen time
@bp.before_request
@login_required
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# User profile page
@bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html',
            title='Home',
            user=current_user,
            key=current_app.config['STRIPE_PUBLISHABLE_KEY'])

# User profile edit
@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Set values on current_user from form
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.zip_code = form.zip_code.data
        current_user.address = form.address.data
        current_user.state = form.state.data
        db.session.commit()
        flash('Success! Your changes have been saved')
        return redirect(url_for('user.profile'))

    elif request.method == 'GET':
        # Set the values on form from current_user
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.zip_code.data = current_user.zip_code
        form.address.data = current_user.address
        form.state.data = current_user.state

    return render_template('user/edit.html', form=form)