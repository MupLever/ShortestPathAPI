## ShortestPathApi

API server that returns the optimal Hamiltonian cycle (chain).

### Endpoints
`/api/v1/shortest_path/` - endpoint for getting the shortest path in the complete graph

### Required request format

```json
{
  "addresses_ids": [4, 5, 6, 7],
  "executor": "string",
  "execution_date": "2024-03-20T19:42:57.980Z"
}
```

### Response format

```json
{
  "total_duration": 218,
  "execution_date": "2024-03-13T23:04:05.853000",
  "created_at": "2024-03-13T20:54:31.044919",
  "updated_at": "2024-03-13T20:54:31.044919",
  "executor": "string",
  "user_id": 1,
  "id": 11,
  "positions": [
    {
      "duration": 0,
      "status": "pending",
      "id": 11,
      "pos": 0,
      "address_id": 4,
      "route_id": 11,
      "address": {
        "district": "Академический",
        "house_number": "1к3с1",
        "city": "Москва",
        "street": "улица Шверника",
        "id": 4
      }
    },
    {
      "duration": 23,
      "status": "pending",
      "id": 12,
      "pos": 1,
      "address_id": 5,
      "route_id": 11,
      "address": {
        "district": "Академический",
        "house_number": "1к3с3Г",
        "city": "Москва",
        "street": "улица Шверника",
        "id": 5
      }
    },
    {
      "duration": 46,
      "status": "pending",
      "id": 13,
      "pos": 2,
      "address_id": 6,
      "route_id": 11,
      "address": {
        "district": "Академический",
        "house_number": "1к4",
        "city": "Москва",
        "street": "улица Шверника",
        "id": 6
      }
    },
    {
      "duration": 65,
      "status": "pending",
      "id": 14,
      "pos": 3,
      "address_id": 7,
      "route_id": 11,
      "address": {
        "district": "Академический",
        "house_number": "2с4",
        "city": "Москва",
        "street": "улица Шверника",
        "id": 7
      }
    },
    {
      "duration": 84,
      "status": "pending",
      "id": 15,
      "pos": 4,
      "address_id": 4,
      "route_id": 11,
      "address": {
        "district": "Академический",
        "house_number": "1к3с1",
        "city": "Москва",
        "street": "улица Шверника",
        "id": 4
      }
    }
  ]
}
```
### Version
python3.8.10

### Dependencies

* fastapi==0.109.0
* pydantic==2.5.3
* uvicorn==0.26.0
* others in [`requirements.txt`](https://github.com/MupLever/ShortestPathApi/blob/master/requirements.txt)
