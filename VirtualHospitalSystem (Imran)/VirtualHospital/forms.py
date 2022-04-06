from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from VirtualHospital.models import Patients, Doctor

class SignUpForm(FlaskForm):
    def validate_username(self, patient_to_check):
        patient = Patients.query.filter_by(username=patient_to_check.data).first()
        if patient:
            raise ValidationError('Username already exist! Please try a different name.')

    def validate_email_address(self, email_address_to_chek):
        email_address = Patients.query.filter_by(email_address=email_address_to_chek.data).first()
        if email_address:
            raise ValidationError('This email is already used for creating a account! Please try another email-address.')

    username = StringField(label='User Name', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    p_num = StringField(label='Phone Number', validators=[DataRequired()])
    age = IntegerField(label='Age', validators=[DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class DoctorSignUpForm(FlaskForm):
    def validate_id(self, doctor_to_check):
        doctor = Doctor.query.filter_by(id=doctor_to_check.data).first()
        if doctor:
            raise ValidationError('This id is already taken by another doctor! Please try a different id.')

    def validate_username(self, doctor_to_check):
        doctor = Doctor.query.filter_by(username=doctor_to_check.data).first()
        if doctor:
            raise ValidationError('Username already exist! Please try a different name.')

    def validate_email(self, doctor_to_check):
        email = Doctor.query.filter_by(email=doctor_to_check.data).first()
        if email:
            raise ValidationError('This email is already used for creating a account! Please try another email-address.')

    username = StringField(label='User Name', validators=[Length(min=4, max=30), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    id = IntegerField(label='Doctor Id', validators=[DataRequired()])
    clas = StringField(label='Specialty', validators=[Length(max=50), DataRequired()])
    phone_number = StringField(label='Phone Number', validators=[Length(max=50), DataRequired()])
    experience = StringField(label='Experience', validators=[Length(max=50), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class SignInForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class SignInFormDoctor(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class RemovePatientForm(FlaskForm):
    submit = SubmitField(label="Remove Patient!")

class AppointmentForm(FlaskForm):
    submit = SubmitField(label="Take Appointment!")

class symptomForm(FlaskForm):
    symptom = StringField(validators=[DataRequired()])
    submit = SubmitField(label='Continue')

class FeedbackForm(FlaskForm):
    owner_feedback = StringField(label='Give Your Feedback', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class UpdateMedicationForm(FlaskForm):
    medication = StringField(label='Medicine', validators=[DataRequired(), Length(min=4, max=1024)])
    dose = StringField(label='Dose', validators=[DataRequired(), Length(min=1, max=1024)])
    submit = SubmitField(label="Update Medication")




