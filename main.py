import json
# import networkx as nx

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field
from requests import request

from utils import graph

app = FastAPI(title="Shortest Path API", version="1.0.0", description="")


# schemas
# class LegalAddress(BaseModel):
#     city
#     street
#     house_number
#     latitude
#     longitude
#
# class Path:
#     metadata
#     id
#     duration
#     distance
#
# class PathLegalAddress:
#     index
#     path_id
#     legal_address_id


class LegalAddress(BaseModel):
    city: str
    street: str = Field()
    house_number: int = Field()
    apartment_number: int
    entrance_number: int
    floor: int


@app.get("/api/v1/shortest_path/")
async def get_shortest_path(legal_addresses: List[LegalAddress]):
    for legal_address in legal_addresses:
        response = request(
            method='POST',
            url='http://localhost:8001/api/v1/geocoder',
            json=json.dumps(legal_address)
        )
        response.json().get('')

    for i in range(0, len(legal_addresses)):
        for j in range(i + 1, len(legal_addresses)):
            response = request(
                method='POST',
                url='http://localhost:8002/api/v1/distance_matrix',
                json=json.dumps([
                        json.dumps(legal_addresses[i]), json.dumps(legal_addresses[j])
                    ])
            )

            response.json().get('')

    return {'shortest_path': 'path'}
