from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user

from services.user_service import UserServices


admin_login = Blueprint('admin_login', __name__)

@admin_login.route('/admin/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = UserServices.get_by_email(email)
            if not user or not user.check_password(password):
                flash("Veuillez compléter correctement les champs « email » et « mot de passe » d'un compte administracteur.")
                return render_template('admin/login.html')
            if not user.isActive or not user.isStaff or not user.isAdmin:
                flash("Veuillez compléter correctement les champs « email » et « mot de passe » d'un compte administracteur.")
                return render_template('admin/login.html')
            login_user(user)
            return redirect(url_for('admin.index'))
    return render_template('admin/login.html')

@admin_login.route('/admin/user/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
