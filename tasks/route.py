from celery import Celery

from app.models import User
from api_v1.addresses.crud import get_addresses_by_id_list
from api_v1.routes import crud
from configs.database import get_session_dependency
from utils import external_api, graph_api


celery = Celery("tasks", broker="redis://localhost:6379")


@celery.task
def create(info: dict, user_id: int) -> None:
    session = next(get_session_dependency())
    user = session.query(User).get(user_id)

    legal_addresses = get_addresses_by_id_list(session, info["addresses_ids"])
    coordinates_dict = external_api.get_coordinates(legal_addresses)
    edges_list = external_api.get_distances(coordinates_dict)
    data = graph_api.get_min_hamiltonian_cycle(edges_list)

    data["executor"] = info["executor"]
    data["execution_date"] = info["execution_date"]

    crud.create_route(session, user, data)
