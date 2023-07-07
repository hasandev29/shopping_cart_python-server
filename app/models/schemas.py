productSchema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "pdtName": {"type": "string"},
    "pdtPrice": {"type": "integer"},
    "pdtDesc": {"type": "string"},
    "pdtCategory": {"type": "string"},
    "pdtImage": {"type": "string"}
  },
  "additionalProperties": False,
  "required": [
    "pdtCategory",
    "pdtName",
    "pdtPrice",
    "pdtDesc",
    "pdtImage"
  ]
}

categorySchema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "catName": {"type": "string"},
    "catImage": {"type": "string"}
  },
  "additionalProperties": False,
  "required": ["catName"]
}

cartSchema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "userId": {"type": "string"},
    "pdtId": {"type": "string"},
    "quantity": {"type": "integer"},
    "price": {"type": "integer"},
    "total": {"type": "integer"}
  },
  "additionalProperties": False,
  "required": [
    "pdtId",
    "quantity",
    "price",
    "total"]
}