from datetime import datetime
from threading import Thread

from sqlalchemy import event, func
from sqlalchemy.dialects import mssql

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName
from ..tpp_Condition.model import tpp_Condition
from ..tpp_ProductImage.model import tpp_ProductImage
from ..tpp_ProductVariation.model import tpp_ProductVariation
from ..tpp_Size.model import tpp_Size


class tpp_Product(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    price = db.Column(mssql.MONEY, default=0, nullable=True)
    stock = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    category_id = db.Column(db.Integer, nullable=True)
    store_id = db.Column(db.BigInteger, nullable=True)

    # tpp_structural = db.relationship("tpp_structural", backref=modelName, lazy="dynamic")
    @property
    def images(self):
        base_url = "http://res.cloudinary.com/insabaaset/"
        images = (
            db.session.query(tpp_ProductImage)
            .filter(tpp_ProductImage.product_id == self.id)
            .all()
        )
        return [
            {
                "id": img.id,
                "product": img.product_id,
                "image": base_url + img.image,
                "is_primary": bool(img.is_primary)
            }
            for img in images
        ]

    @property
    def variations(self):
        variations = (
            db.session.query(tpp_ProductVariation)
            .filter(tpp_ProductVariation.product_id == self.id)
            .all()
        )

        result = []
        for v in variations:
            size = tpp_Size.query.get(v.size_id)
            condition = tpp_Condition.query.get(v.condition_id)
            result.append({
                "id": v.id,
                "product": v.product_id,
                "size": {"id": size.id, "name": size.name} if size else None,
                "condition": {"id": condition.id, "name": condition.name} if condition else None,
            })
        return result

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "stock": self.stock,
            "category": self.category_id,
            "is_active": bool(self.is_active),
            "created_at": self.created_at.isoformat() + "Z" if self.created_at else None,
            "images": self.images,
            "variations": self.variations,
        }

# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_Product)
#
#
# @event.listens_for(tpp_Product, 'before_insert')
# def check_unit_privilege_insert(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_Product, 'before_update')
# def check_unit_privilege_delete(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_Product, 'before_delete')
# def check_unit_privilege_update(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# # AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
# @event.listens_for(tpp_Product, 'after_insert')
# def insert_activity_insert(mapper, connection, target):
#     access_token = current_user['access_token']
#     origin = current_user['origin']
#     data = {
#         "type": 'post',
#         'endpoint_path': f'{apiPath}',
#         'data_id': target.id,
#         'subject': crudTitle,
#         'origin': origin,
#         "attributes": {
#             'data': row2dict(target)
#         }
#     }
#     thread = Thread(target=insert_user_activity, args=(data, access_token,))
#     thread.start()
#     thread.join()
#
#
# @event.listens_for(tpp_Product, 'after_update')
# def insert_activity_update(mapper, connection, target):
#     access_token = current_user['access_token']
#     origin = current_user['origin']
#     data = {
#         "type": 'put',
#         'endpoint_path': f'{apiPath}',
#         'data_id': target.id,
#         'subject': crudTitle,
#         'origin': origin,
#         "attributes": {
#             'data': row2dict(target)
#         }
#     }
#     thread = Thread(target=insert_user_activity, args=(data, access_token,))
#     thread.start()
#     thread.join()
#
#
# @event.listens_for(tpp_Product, 'after_delete')
# def insert_activity_delete(mapper, connection, target):
#     access_token = current_user['access_token']
#     origin = current_user['origin']
#     data = {
#         "type": 'delete',
#         'endpoint_path': f'{apiPath}',
#         'data_id': target.id,
#         'subject': crudTitle,
#         'origin': origin,
#         "attributes": {
#             'data': row2dict(target)
#         }
#     }
#     thread = Thread(target=insert_user_activity, args=(data, access_token,))
#     thread.start()
#     thread.join()