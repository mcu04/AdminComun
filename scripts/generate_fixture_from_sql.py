import re
import json

def extract_documentacion_data(sql_file_path, start_line=746, end_line=942):
    documentacion_data = []
    current_line = 0
    
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            current_line += 1
            if current_line < start_line:
                continue
            if current_line > end_line:
                break
                
            # Buscar líneas que contengan datos de documentación
            # El patrón busca líneas que comienzan con un número seguido de tab
            match = re.match(r'(\d+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t', line.strip())
            if match:
                id_doc, tipo, categoria, titulo = match.groups()
                
                # Crear el objeto de fixture
                fixture_object = {
                    "model": "seguimientodocumentos.documentacion",
                    "pk": int(id_doc),
                    "fields": {
                        "tipo": tipo.strip(),
                        "categoria": categoria.strip(),
                        "titulo_documento": titulo.strip(),
                        "comunidad": None
                    }
                }
                documentacion_data.append(fixture_object)
    
    return documentacion_data

def generate_fixture():
    # Ruta al archivo SQL
    sql_file_path = '../ResDocumentacion.sql'
    
    # Extraer datos
    fixture_data = extract_documentacion_data(sql_file_path)
    
    # Guardar en archivo JSON
    output_path = '../fixtures/initial_documentacion.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(fixture_data, f, ensure_ascii=False, indent=2)
    
    print(f"Se han generado {len(fixture_data)} registros en el archivo {output_path}")

if __name__ == "__main__":
    generate_fixture()