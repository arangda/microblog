from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField,HiddenField
from wtforms.validators import DataRequired,Length,Email,Optional,URL
from app.shares.models import Category


class ShareForm(FlaskForm):
    name = StringField('Name')
    code = StringField('Code',validators=[DataRequired()])
    category = SelectField('Category',coerce=int,default=0)
    markdown = TextAreaField('Content')
    submit = SubmitField('提交')
    
    def __init__(self,*args,**kwargs):
        super(ShareForm,self).__init__(*args,**kwargs)
        self.category.choices = [(category.id,category.name)
                                for category in Category.query.order_by(Category.name).all()
        ]


class CategoryForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,30)])
    english_name = StringField('英文名称')
    submit = SubmitField()

    #def validate_name(self,field):
    #    if Category.query.filter_by(name=field.data).first():
    #        raise ValidationError('类名已经存在')


class TagForm(FlaskForm):
    tag = StringField('添加Tag(用"#"隔开)',validators=[Optional(),Length(0,64)])
    submit = SubmitField()