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
    stock_maximo = IntegerField('Stock máximo', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired()])
    ubicacion = StringField('Ubicación')
    referencia = StringField('Referencia')
    color = StringField('Color')
    proveedores = SelectMultipleField('Proveedores', coerce=int) 
    submit = SubmitField('Guardar')
    
class ProveedorForm(FlaskForm):
    nombre_empresa = StringField('Nombre de empresa', validators=[DataRequired()])
    cif = StringField('CIF', validators=[DataRequired()])
    telefono = StringField('Teléfono')
    direccion = StringField('Dirección')
    email = StringField('Email', validators=[Email()])
    descuento = FloatField('Descuento (%)')
    iva = FloatField('IVA (%)', default=21.0)
    precio_base = FloatField('Precio base')
    submit = SubmitField('Guardar')