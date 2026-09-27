from fastapi import Depends

from src.repositories.acme_repository import AcmeRepository
from src.services.acme_service import AcmeService


def get_repository() -> AcmeRepository:
    """
    Dépendance pour obtenir une instance d'AcmeRepository.
    """
    return AcmeRepository()

def get_service(repository: AcmeRepository = Depends(get_repository)) -> AcmeService:
    """
    Dépendance pour obtenir une instance d'AcmeService.
    """
    return AcmeService(repository)

