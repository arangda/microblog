from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField,HiddenField
from wtforms.validators import DataRequired,Length,Email,Optional,URL
from app.shares.models import Category


class ShareForm(FlaskForm):
    name = StringField('Name')
    code = StringField('Code',validators=[DataRequired()])
    category = SelectField('Category',coerce=int,default=1)
    content = TextAreaField('Content')
    submit = SubmitField('提交')
    
    def __init__(self,*args,**kwargs):
        super(ShareForm,self).__init__(*args,**kwargs)
        self.category.choices = [(category.id,category.name)
                                for category in Category.query.order_by(Category.name).all()
        ]