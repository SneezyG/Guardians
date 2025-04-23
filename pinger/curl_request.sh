curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sneezyg",
    "password": "gbolahan30"
}' | jq

{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1NDM4NDE5LCJpYXQiOjE3NDU0Mjg2OTgsImp0aSI6IjY2Yjk4ZGIwNTBhYjQ4MDVhYzUxNWJjYTc5ZTA0N2ViIiwidXNlcl9pZCI6MX0.Olf1iQM58bj16dfWflgODgKVmoFoYH-NywL6YkkNFEU",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NTUyMTIxOSwiaWF0IjoxNzQ1NDM0ODE5LCJqdGkiOiJlNTRiYzE4NDk0ZTk0MDg4YWNkNGU4NTUxMGYwYTdkYyIsInVzZXJfaWQiOjF9.4D6RZuXKN0WfL7terp5MEDQWK0mMAYdLrGU6XzyB2wU"
}

curl -X POST http://localhost:8000/api/auth/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "access token"
}' | jq


curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "refresh token"
}' | jq


curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your_refresh_token_here"
}' | jq


curl -G http://localhost:8000/api/alerts/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "accept: application/json" \
  --data-urlencode "category=fire" \
  --data-urlencode "status=confirmed" \
  --data-urlencode "severity=medium" \
  | jq


curl -G http://localhost:8000/api/alerts/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1NDM4NDE5LCJpYXQiOjE3NDU0Mjg2OTgsImp0aSI6IjY2Yjk4ZGIwNTBhYjQ4MDVhYzUxNWJjYTc5ZTA0N2ViIiwidXNlcl9pZCI6MX0.Olf1iQM58bj16dfWflgODgKVmoFoYH-NywL6YkkNFEU" \
  --data-urlencode "limit=5" \
  --data-urlencode "offset=10" \
  | jq


curl -X POST http://localhost:8000/api/alerts/create \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "fire",
    "location": "Warehouse A",
    "severity": "high",
    "description_notes": "Fire detected near chemical storage."
  }' | jq


curl -X GET http://localhost:8000/api/alerts/latest/ \
-H "Authorization: Bearer your_access_token_here" \
  -H "accept: application/json" \
  | jq


curl -X GET http://localhost:8000/api/alerts/48d21a46-4cd6-494f-a633-05cb19bd5fa0/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Accept: application/json" \
  | jq


curl -X GET http://localhost:8000/api/alerts/user/10/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Accept: application/json" \
  | jq


curl -X PATCH http://localhost:8000/api/alerts/48d21a46-4cd6-494f-a633-05cb19bd5fa0/update/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed",
    "resolution_notes": "Alert confirmed by site supervisor."
  }' \
  | jq


curl -X GET http://localhost:8000/api/audit/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Accept: application/json" \
  | jq


curl -G http://localhost:8000/api/audit/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Accept: application/json" \
  --data-urlencode "action=resolved" \
  --data-urlencode "timestamp__gte=2025-02-01" \
  | jq


curl -G http://localhost:8000/api/audit/report/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Accept: application/json" \
  --data-urlencode "action=resolved" \
  --data-urlencode "timestamp__gte=2025-02-01" \
  | jq


curl -X GET http://localhost:8000/api/safety_tips/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Accept: application/json" \
  | jq


curl -X PUT http://localhost:8000/api/alerts/bulk/update/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Content-Type: application/json" \
  -d '{
        "alerts": [
          { "id": "aec65be4-8871-4f88-a1ab-efa0dd28ddf5", "status": "resolved" },
          { "id": "47f3037f-3856-48a8-ba32-13b07922e5b6", "status": "dismissed" },
          { "id": "db5b685a-9e34-4187-b1c9-053cf840ae99", "status": "comfirmed" }
        ]
      }' \
    | jq


