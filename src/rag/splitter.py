from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(documents: list[Document], chunk_size: int = 800, chunk_overlap: int = 150) -> list[Document]:
    
    """
    Divise une liste de Document en plusieurs chunks de taille spécifiée avec un chevauchement donné.

    Args:
        documents (list[Document]): Liste de Document à diviser.
        chunk_size (int, optional): Taille maximale de chaque chunk. Par défaut à 800.
        chunk_overlap (int, optional): Chevauchement entre les chunks. Par défaut à 150.

    Returns:
        list[Document]: Liste de Document divisés en chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return splitter.split_documents(documents)