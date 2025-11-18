from flask_restx import fields

moduleTitle = ''
crudTitle = 'tpp_ProductImage'
apiPath = 'tpp_ProductImage'
modelName = 'tpp_ProductImage'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "image": fields.String(required=True, min_length=5, max_length=200, ),
    "is_primary": fields.Integer(required=False, min_length=5, max_length=100, ),
    "product_id": fields.Integer(required=False, min_length=5, max_length=100, ),
}
uniqueField = [""]
searchField = [""]
sortField = ["id"]
filterField = [""]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'