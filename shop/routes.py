from shop import app
from shop.models import Item, User
from shop.forms import RegisterForm, LoginForm, PurchaseItemForm, AddItemForm, DeleteUserForm
from flask import render_template, redirect, url_for, flash, request
from shop import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/shop", methods=['GET', 'POST'])
@login_required
def shop_page():
    form = PurchaseItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item = Item.query.filter_by(name=purchased_item).first()
        if p_item:
            p_item.owner = current_user.id
            db.session.commit()
            flash("Поздравляем с покупкой!", category='success')
        return redirect(url_for('shop_page'))
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        return render_template('shop.html', items=items, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password1.data
                        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Вы были успешно зарегистрированы как {new_user.username}!', category='success')
        return redirect(url_for('shop_page'))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f"Ошибка при регистрации пользователя: {err_msg}", category='danger')
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'{user.username}, с возвращением!', category='success')
            return redirect(url_for('shop_page'))
        else:
            flash('Логин и пароль не совпадают', category='danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash('Вы вышли из личного кабинета', category='info')
    return render_template('home.html')


@app.route("/admin", methods=['GET', 'POST'])
def admin_page():
    form1 = DeleteUserForm()
    form = AddItemForm()
    users = User.query.filter_by()
    if request.form.get('submit') == "Удалить":
        if request.method == 'POST':
            deleted_user = request.form.get('deleted_user')
            d_user = User.query.filter_by(username=deleted_user).first()
            if d_user:
                if d_user == current_user:
                    logout_user()
                db.session.delete(d_user)
                db.session.commit()
                flash("Вы удалили пользователя", category='success')
    if request.form.get('submit') == 'Add':
        if form.validate_on_submit():
            new_item = Item(name=form.name.data,
                            desc=form.desc.data,
                            size=form.size.data,
                            price=form.price.data,
                            owner=None
                            )
            db.session.add(new_item)
            db.session.commit()
            flash(f'Вы успешно добавили {new_item.name}!', category='success')
            form = AddItemForm(formdata=None)
        if form.errors:
            for err_msg in form.errors.values():
                flash(f"Ошибка добавления: {err_msg}", category='danger')
    return render_template('admin.html', form=form, form1=form1, users=users)
