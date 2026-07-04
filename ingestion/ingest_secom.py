import pandas as pd 
import shutil
from pathlib import Path
from datetime import datetime

RAW_DATA_DIR = Path("data/raw")
INGESTED_DIR = Path("data/ingested")

def validar_archivos_fuente():
    archivo_datos = RAW_DATA_DIR / "secom.data"
    archivo_labels = RAW_DATA_DIR / "secom_labels.data"
    
    if not archivo_datos.exists():
        raise FileNotFoundError(f"No se encontró: {archivo_datos}")
    if not archivo_labels.exists():
        raise FileNotFoundError(f"No se encontró: {archivo_labels}")
    
    print("Archivos fuente encontrados.")
    return archivo_datos, archivo_labels

def copiar_a_ingested(archivo_datos, archivo_labels):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    carpeta_destino = INGESTED_DIR / timestamp
    carpeta_destino.mkdir(parents=True, exist_ok=True)
    
    shutil.copy(archivo_datos, carpeta_destino / "secom.data")
    shutil.copy(archivo_labels, carpeta_destino / "secom_labels.data")
    
    print(f"Datos copiados a: {carpeta_destino}")
    return carpeta_destino

def main():
    print("**** Iniciando ingesta de datos SECOM ****")
    try:
        archivo_datos, archivo_labels = validar_archivos_fuente()
        carpeta_destino = copiar_a_ingested(archivo_datos, archivo_labels)
        
        #Validacion extra, confirma sque el archivo copiado se puede leer con pandas
        
        df_check = pd.read_csv(carpeta_destino / "secom.data", sep=' ', header=None)
        print(f"Validación exitosa: {df_check.shape[0]} filas y {df_check.shape[1]} columnas.")
        
        print("**** Ingesta completada exitosamente ****")
        
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}") 


if __name__ == "__main__":
    main()                
        