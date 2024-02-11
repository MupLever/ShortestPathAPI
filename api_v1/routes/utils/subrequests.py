from requests import request


async def get_coordinates(legal_addresses) -> list:
    address_list = []
    for legal_address in legal_addresses:
        response = request(
            url="http://localhost:8001/api/v1/geocoder/",
            method="POST",
            json=legal_address.model_dump(),
        )
        address_list.append(response.json().get("coordinates"))

    return address_list


async def get_distances(legal_addresses, address_list) -> list:
    data = []

    for i in range(0, len(address_list)):
        for j in range(i + 1, len(address_list)):
            json_body = {
                "first_address": {
                    "latitude": address_list[i]["lat"],
                    "longitude": address_list[i]["lng"],
                },
                "second_address": {
                    "latitude": address_list[j]["lat"],
                    "longitude": address_list[j]["lng"],
                },
            }
            response = request(
                method="POST",
                url="http://localhost:8002/api/v1/distance_matrix/",
                json=json_body,
            )
            distance = int(response.json().get("distance"))
            edge = (
                f"{legal_addresses[i]}",
                f"{legal_addresses[j]}",
                distance,
            )
            data.append(edge)

            edge = (
                f"{legal_addresses[j]}",
                f"{legal_addresses[i]}",
                distance,
            )
            data.append(edge)

    return data
