import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from app import db
from datetime import datetime,timezone
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin,db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    username: so.Mapped[str]=so.mapped_column(sa.String(60),index=True,unique=True)
    email: so.Mapped[str]=so.mapped_column(sa.String(60),index=True,unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    orders: so.WriteOnlyMapped["Order"]=so.relationship(back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
    
class Order(db.Model):
    id: so.Mapped[int]=so.mapped_column(primary_key=True)
    ord_id: so.Mapped[str]=so.mapped_column(sa.String(100),index=True,unique=True,default=lambda: str(uuid.uuid4()))
    amount: so.Mapped[int]=so.mapped_column(sa.Integer)
    status: so.Mapped[str]=so.mapped_column(sa.String(20),default="unpaid")
    reciptent_username: so.Mapped[str]=so.mapped_column(sa.String(25))
    created_at: so.Mapped[datetime]=so.mapped_column(index=True,default=lambda:datetime.now(timezone.utc))
    user_id: so.Mapped[int]=so.mapped_column(sa.ForeignKey(User.id),index=True)
    user: so.Mapped[User]=so.relationship(back_populates="orders")
    