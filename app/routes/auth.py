import random
import string
from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, OTPForm, ResetPasswordForm
from ..models import User
from ..extensions import db, bcrypt
from ..utils import send_email
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('auth', __name__)

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        # Send confirmation email
        send_email('Welcome to Our Application',
                   recipients=[user.email],
                   text_body=render_template('welcome_email.txt', username=user.username),
                   html_body=render_template('welcome_email.html', username=user.username))
        
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account', user=current_user)

@bp.route("/forgot", methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            otp = ''.join(random.choices(string.digits, k=6))
            session['otp'] = otp
            session['email'] = form.email.data
            send_email('Your OTP Code', recipients=[user.email], text_body=f'Your OTP code is {otp}', html_body=f'<p>Your OTP code is <strong>{otp}</strong></p>')
            flash('An OTP has been sent to your email.', 'info')
            return redirect(url_for('auth.verify_otp'))
        else:
            flash('Email not found', 'danger')
    return render_template('forgot_password.html', title='Forgot Password', form=form)

@bp.route("/otp", methods=['GET', 'POST'])
def verify_otp():
    form = OTPForm()
    if form.validate_on_submit():
        otp = session.get('otp')
        if otp and form.otp.data == otp:
            session['otp_verified'] = True
            flash('OTP verified. You can now reset your password.', 'success')
            return redirect(url_for('auth.reset_password'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
    return render_template('verify_otp.html', title='Verify OTP', form=form)


@bp.route("/reset", methods=['GET', 'POST'])
def reset_password():
    if not session.get('otp_verified'):
        flash('You must verify the OTP before resetting your password.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = session.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            # Clear sensitive session data
            session.pop('otp_verified', None)
            session.pop('email', None)
            flash('Your password has been reset. You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occurred. Please try again.', 'danger')
    return render_template('reset_password.html', title='Reset Password', form=form)

