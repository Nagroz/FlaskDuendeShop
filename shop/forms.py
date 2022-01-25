from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from shop.models import User, Item


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label="Enter")


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Данный пользователь уже существует")

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Данный email уже зарегистрирован")

    username = StringField(label='Username:', validators=[Length(min=2, max=20), DataRequired()])
    email = StringField(label='E-Mail address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=7, max=20), DataRequired()])
    password2 = PasswordField(label='Confirm password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField()


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Купить")


class DeleteUserForm(FlaskForm):
    submit = SubmitField(label="Удалить")


class AddItemForm(FlaskForm):
    def validate_name(self, name_to_check):
        item = Item.query.filter_by(name=name_to_check.data).first()
        if item:
            raise ValidationError("Данный item уже существует")

    name = StringField(label='Item name:', validators=[Length(min=2, max=20), DataRequired()])
    desc = StringField(label='Item description:', validators=[Length(min=2, max=20), DataRequired()])
    size = StringField(label='Item size:', validators=[Length(min=1, max=20), DataRequired()])
    price = IntegerField(label='Item price:', validators=[NumberRange(min=100), DataRequired()])
    submit = SubmitField(label="Add")
