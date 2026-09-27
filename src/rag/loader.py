from pathlib import Path

from langchain_core.documents import Document


# chemin vers le répertoire contenant les documents
DOCUMENTS_DIR = Path("data/acme_logistics/documents")

# charge un fichier et retourne une liste de Document
def load_file(path: str | Path, encoding: str = "utf-8",) -> list[Document]:

    path = Path(path)

    return [
        Document(
            page_content=path.read_text(encoding=encoding),
            metadata={
                "source": str(path),
                "file_name": path.name,
            },
        )
    ]

# charge tous les fichiers d'un répertoire et retourne une liste de Document
def load_directory(dir_path: str | Path, glob: str = "**/*.md",) -> list[Document]:

    documents = []

    for file in sorted(Path(dir_path).glob(glob)):
        if file.is_file():
            documents.extend(load_file(file))

    return documents