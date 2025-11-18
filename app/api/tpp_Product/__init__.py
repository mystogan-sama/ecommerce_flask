from flask_restx import fields

from app.api import api

moduleTitle = ''
crudTitle = 'tpp_Product'
apiPath = 'tpp_Product'
modelName = 'tpp_Product'

size_model = api.model('tpp_Size', {
    'id': fields.Integer,
    'name': fields.String,
})
api.models['tpp_Size'] = size_model  # pastikan terdaftar

condition_model = api.model('tpp_Condition', {
    'id': fields.Integer,
    'name': fields.String,
})
api.models['tpp_Condition'] = condition_model

product_image_model = api.model('tpp_ProductImage', {
    'id': fields.Integer,
    'product': fields.Integer,
    'image': fields.String,
    'is_primary': fields.Boolean,
})
api.models['tpp_ProductImage'] = product_image_model

variation_model = api.model('tpp_ProductVariation', {
    'id': fields.Integer,
    'product': fields.Integer,
    'size': fields.Nested(size_model),
    'condition': fields.Nested(condition_model),
})
api.models['tpp_ProductVariation'] = variation_model

respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "name": fields.String(required=True, min_length=5, max_length=200, ),
    "description": fields.String(required=False, min_length=5, max_length=100, ),
    "price": fields.Fixed(example=1, ),
    "stock": fields.Integer(example=1, ),
    "is_active": fields.Integer(example=1, ),
    "created_at": fields.DateTime(readonly=True, example="2023-01-01T00:00:00"),
    "category_id": fields.Integer(example=1, ),
    "store_id": fields.Integer(example=1, ),
    "images": fields.List(fields.Nested(product_image_model)),
    "variations": fields.List(fields.Nested(variation_model)),
}
uniqueField = [""]
searchField = ["name"]
sortField = ["id"]
filterField = ["category_id"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'