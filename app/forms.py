from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,TextAreaField,IntegerField,FloatField,SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirmar_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    rol = SelectField('Rol', choices=[('cliente', 'Cliente'), ('admin', 'Administrador')])
    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')
    
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired()])
    ubicacion = StringField('Ubicación')
    referencia = StringField('Referencia')
    color = StringField('Color')
    proveedores = SelectMultipleField('Proveedores', coerce=int) 
    submit = SubmitField('Guardar')