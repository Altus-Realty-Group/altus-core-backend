@echo off
curl.exe -k -i -X POST https://altus-core-staging-func.azurewebsites.net/api/assets/ingest -H "Content-Type: application/json" -H "x-altus-org-id: d290f1ee-6c54-4b01-90e6-d701748f0851" -d "{\"source\":\"MANUAL\",\"raw\":{\"ping\":\"fix-05\"},\"asset\":{\"name\":\"FIX-05\",\"asset_type\":\"PROPERTY\",\"status\":\"ACTIVE\"}}"
