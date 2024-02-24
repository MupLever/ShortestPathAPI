def to_list_legal_address(data: dict) -> list:
    return [
        {"address": address_str_to_dict(el["address"]), "duration": el["duration"]}
        for el in data
    ]


def address_str_to_dict(address: str) -> dict:
    values = address.split(', ')
    keys = ["city", "district", "street", "house_number", "apartment_number", "entrance_number", "floor"]
    return dict(zip(keys, values))
