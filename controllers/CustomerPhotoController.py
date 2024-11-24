# @customer_photo_bp.route('/listar', methods=['GET'])
# @jwt_required()
# def get_all_photos():
#     photos = customerPhotoRepository.get_all()
#     response = Responses.success(
#         code=0,
#         data=photos,
#         description='Fotos listadas correctamente'
#     )
#     return jsonify(response)

# @customer_photo_bp.route('/buscar/<int:customer_id>', methods=['GET'])
# @jwt_required()
# def get_photos_by_customer_id(customer_id):
#     photos = customerPhotoRepository.get_by_customer_id(customer_id)
#     if photos:
#         response = Responses.success(
#             code=0,
#             data=photos,
#             description='Fotos encontradas'
#         )
#     else:
#         response = Responses.error(
#             code=1,
#             description=f'No se encontraron fotos para el cliente con ID {customer_id}'
#         )
#     return jsonify(response)

# @customer_photo_bp.route('/registrar', methods=['POST'])
# @jwt_required()
# def create_photo():
#     data = request.json
#     new_photo = customerPhotoRepository.create(
#         customer_id=data['customer_id'],
#         photo_type=data['photo_type'],
#         photo_url=data['photo_url']
#     )
#     response = Responses.success(
#         code=0,
#         data=new_photo,
#         description='Foto creada correctamente'
#     )
#     return jsonify(response)
