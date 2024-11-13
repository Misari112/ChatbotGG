def transform_structure(original_data):
    # Crear un nuevo diccionario para almacenar la estructura transformada
    transformed_data = {}
    
    # Iterar sobre las materias en la estructura original
    for key, value in original_data.items():
        # Excluir el campo 'state' de la transformación
        if key == 'state':
            continue
        
        # Crear una nueva entrada sin el campo 'materia'
        transformed_data[key] = {
            'creditos': value.get('creditos'),
            'valor': value.get('valor')
        }
    
    return transformed_data