import uvicorn
# import networkx as nx

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from requests import request

from utils.graph import Graph

app = FastAPI(title="Shortest Path API", version="1.0.0", description="")


class LegalAddress(BaseModel):
    city: str
    street: str
    house_number: int
    apartment_number: int
    entrance_number: int
    floor: int

    def __repr(self):
        return f"{self.city}, {self.street}, {self.house_number}, {self.apartment_number}"

    def __str__(self):
        return f"{self.city}, {self.street}, {self.house_number}, {self.apartment_number}"


@app.post("/api/v1/shortest_path/")
async def get_shortest_path(legal_addresses: List[LegalAddress]):
    address_list = []
    for legal_address in legal_addresses:
        response = request(
            url="http://localhost:8001/api/v1/geocoder/",
            method="POST",
            json={
                "city": legal_address.city,
                "street": legal_address.street,
                "house_number": legal_address.house_number,
                "apartment_number": legal_address.apartment_number,
                "entrance_number": legal_address.entrance_number,
                "floor": legal_address.floor,
            }
        )
        address_list.append(response.json().get("coordinates"))

    data = []

    for i in range(0, len(address_list)):
        for j in range(i + 1, len(address_list)):
            response = request(
                method="POST",
                url="http://localhost:8002/api/v1/distance_matrix/",
                json={
                    "first_address": {
                        "latitude": address_list[i]["lat"],
                        "longitude": address_list[i]["lng"]
                    },
                    "second_address": {
                        "latitude": address_list[j]["lat"],
                        "longitude": address_list[j]["lng"]
                    }
                }
            )
            distance = int(response.json().get("distance"))
            edge = (f"{legal_addresses[i]}", f"{legal_addresses[j]}", distance,)
            data.append(edge)

            edge = (f"{legal_addresses[j]}", f"{legal_addresses[i]}", distance,)
            data.append(edge)

    graph = Graph(data)
    msg, data = graph.find_hamiltonian_cycle()
    return {
        "message": msg,
        "shortest_path": data
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
