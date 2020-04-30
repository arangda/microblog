from app import db
from datetime import datetime


tagging = db.Table('tagging',
                    db.Column('share_id',db.Integer,db.ForeignKey('share.id')),
                    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'))
)
class Share(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),index=True,unique=True)
    code = db.Column(db.String(20),unique=True)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    intro = db.Column(db.Text(16777216), nullable=False)
    markdown = db.Column(db.Text(16777216), nullable=True)
    can_comment = db.Column(db.Boolean,default=True)
    views = db.Column(db.Integer,default=0)
    
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',back_populates='shares')
    comments = db.relationship('Comment',back_populates='share',cascade='all,delete-orphan')
    
    tags = db.relationship('Tag',secondary=tagging,back_populates='shares')

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True)
    english_name = db.Column(db.String(50),unique=True,index=True)
    reviewed = db.Column(db.Boolean,default=False)
    shares = db.relationship('Share',back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        shares = self.shares[:]
        for share in shares:
            share.category = default_category
        db.session.delete(self)
        db.session.commit()


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean,default=False)
    reviewed = db.Column(db.Boolean,default=False)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)

    replied_id = db.Column(db.Integer,db.ForeignKey('comment.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('share.id'))

    share = db.relationship('Share',back_populates='comments')
    replies = db.relationship('Comment',back_populates='replied',cascade='all,delete-orphan')
    replied = db.relationship('Comment',back_populates='replies',remote_side=[id])


class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),index=True,unique=True)
    english_name = db.Column(db.String(50),unique=True,index=True)
    recommend = db.Column(db.Boolean,default=False)
    shares = db.relationship('Share',secondary=tagging,back_populates='tags')