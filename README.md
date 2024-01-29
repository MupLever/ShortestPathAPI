## ShortestPathApi

API server that returns the optimal Hamiltonian cycle (chain).

### Endpoints
`/api/v1/shortest_path/`

### Required request format

```json
[
  {
    "city": "Moscow",
    "street": "Vladimirskya",
    "house_number": 24,
    "apartment_number": 130,
    "entrance_number": 5,
    "floor": 3
  },
  {
    "city": "ST",
    "street": "Lenina",
    "house_number": 114,
    "apartment_number": 2007,
    "entrance_number": 1,
    "floor": 10
  },
  {
    "city": "Irkutsk",
    "street": "Deputatskya",
    "house_number": 7,
    "apartment_number": 80,
    "entrance_number": 2,
    "floor": 10
  }
]
```

### Version
python3.8.10

### Dependencies

* fastapi==0.109.0
* pydantic==2.5.3
* uvicorn==0.26.0
* others in [`requirements.txt`](https://github.com/MupLever/ShortestPathApi/blob/master/requirements.txt)
