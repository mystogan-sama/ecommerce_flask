from flask_restx import fields


moduleTitle = ''
crudTitle = 'tpp_ProductVariation'
apiPath = 'tpp_ProductVariation'
modelName = 'tpp_ProductVariation'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "condition_id": fields.Integer(required=False, min_length=5, max_length=100, ),
    "product_id": fields.Integer(required=False, min_length=5, max_length=100, ),
    "size_id": fields.Integer(required=False, min_length=5, max_length=100, ),
}
uniqueField = ["name"]
searchField = ["name"]
sortField = ["id"]
filterField = []
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'