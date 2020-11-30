from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired,ValidationError,Length,Email,EqualTo,Regexp,Required
from blogepedia.model import Users,Post
from flask_login import current_user 


# to add the regexp for password validation
class RegistrtionForm(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired(),Length(max=20,min=3)],render_kw={"placeholder": "Username"})
    email = StringField(label='Email',validators=[DataRequired(),Email()],render_kw={"placeholder": "Email"})
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=6)],render_kw={"placeholder": "Password"})
    confirmPassword = PasswordField(label='Confirm Password',validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    # checking if the user already exists
    def validate_username(self,username):
       user = Users.query.filter_by(username=username.data).first()
       if user:
          raise ValidationError('The username is taken.Please choose a different one.')
      
    def validate_username(self,email):
       email = Users.query.filter_by(email=email.data).first()
       if email:
          raise ValidationError('The email already exists.Please choose a different one.')



class Loginform(FlaskForm):
    email = StringField(label='Email',validators=[DataRequired(),Email()],render_kw={"placeholder": "Email"})
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=6)],render_kw={"placeholder": "Password"})
    remember= BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountInfo(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired(),Length(max=20,min=3)],render_kw={"placeholder": "Username"})
    email = StringField(label='Email',validators=[DataRequired(),Email()],render_kw={"placeholder": "Email"})
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Save Changes')


    def validate_username(self,username):
       if username.data != current_user.username:
          user = Users.query.filter_by(username=username.data).first()
          if user:
             raise ValidationError('The username is taken.Please choose a different one.')
      

    def validate_email(self,email):
       if email.data != current_user.email:
          user = Users.query.filter_by(email=email.data).first()
          if user:
             raise ValidationError('The email already exists.Please choose a different one.')
   
class NewPost(FlaskForm):
   title = StringField('Title',validators=[DataRequired(),Length(max=100)],render_kw={"placeholder": "Title"})
   content = TextAreaField('Content',validators=[DataRequired()],render_kw={"placeholder": "Content"})
   img_file = FileField('Update Image',validators=[FileAllowed(['jpg','png'],'Only jpg and png format allowed')],render_kw={"placeholder": "Image"})
   submit =SubmitField('Post')


    


