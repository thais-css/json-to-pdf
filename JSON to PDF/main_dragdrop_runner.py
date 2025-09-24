import os
import sys
import tarfile
import subprocess
import shutil
from datetime import datetime

def log_error(message):
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "error.log")
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def clean_data_folder(data_path):
    try:
        for item in os.listdir(data_path):
            item_path = os.path.join(data_path, item)
            if os.path.isdir(item_path):
                subprocess.run(["rm", "-rf", item_path])
            elif os.path.isfile(item_path):
                os.remove(item_path)
    except Exception as e:
        log_error(f"❌ Failed to clean data folder: {e}")
        raise

def extract_tar_gz(tar_path, extract_to):
    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=extract_to)
    except Exception as e:
        log_error(f"❌ Failed to extract tar.gz file: {e}")
        raise

def run_script(script_name):
    try:
        script_dir = os.path.join(os.path.dirname(__file__), "scripts")
        script_path = os.path.join(script_dir, script_name)
        subprocess.run(["python3", script_path], cwd=script_dir, check=True)
    except subprocess.CalledProcessError as e:
        log_error(f"❌ Script {script_name} failed: {e}")
        raise

def open_output_folder():
    output_path = os.path.join(os.path.dirname(__file__), "output")
    subprocess.run(["open", output_path])


def move_existing_data_folders(output_path):
    old_files_path = os.path.join(output_path, "Old Files")
    os.makedirs(old_files_path, exist_ok=True)

    for item in os.listdir(output_path):
        item_path = os.path.join(output_path, item)
        if item.endswith("_data") and os.path.isdir(item_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_folder_name = f"{item}_{timestamp}"
            new_folder_path = os.path.join(old_files_path, new_folder_name)
            try:
                shutil.move(item_path, new_folder_path)
                print(f"📦 Pasta antiga movida para: {new_folder_path}")
            except Exception as e:
                log_error(f"Erro ao mover pasta antiga '{item_path}': {e}")



def main():
    if len(sys.argv) != 2:
        print("Arraste um arquivo .tar.gz sobre o app para iniciar.")
        return

    tar_input = sys.argv[1]

    if not tar_input.endswith(".tar.gz"):
        print("⚠️ Arquivo inválido. Por favor, arraste um .tar.gz.")
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data")

    try:
        print("🔁 Limpando pasta /data...")
        clean_data_folder(data_path)

        print("📦 Extraindo arquivo...")

        # Cria uma subpasta com o nome do arquivo tar
        folder_name = os.path.basename(tar_input).replace(".tar.gz", "")
        extract_target = os.path.join(data_path, folder_name)
        os.makedirs(extract_target, exist_ok=True)

        extract_tar_gz(tar_input, extract_target)


        # Mover pastas *_data antigas antes de gerar novas
        output_path = os.path.join(os.path.dirname(__file__), "output")
        move_existing_data_folders(output_path)

        print("📄 Gerando conteúdo...")
        run_script("generate_content_pdf.py")


        print("📑 Gerando índice...")
        run_script("generate_index_pdf.py")

        print("📚 Mesclando PDFs...")
        run_script("merge_pdfs.py")

        print("✅ Processo concluído. Abrindo pasta output...")
        open_output_folder()

    except Exception as e:
        print("❌ Ocorreu um erro. Verifique logs/error.log para detalhes.")
        log_error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
