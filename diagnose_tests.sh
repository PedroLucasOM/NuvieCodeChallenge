#!/bin/bash

echo "=== DIAGNÓSTICO DETALHADO DOS TESTES ===" > test_diagnosis.log
echo "Data: $(date)" >> test_diagnosis.log
echo "" >> test_diagnosis.log

echo "=== TESTE DE AUTENTICAÇÃO ESPECÍFICO ===" >> test_diagnosis.log
pytest tests/test_auth.py::TestAuthEndpoints::test_register_user_success -v -s --tb=long >> test_diagnosis.log 2>&1
echo "" >> test_diagnosis.log

echo "=== TESTE DE PACIENTE ESPECÍFICO ===" >> test_diagnosis.log
pytest tests/test_patient_service.py::test_create_patient -v -s --tb=long >> test_diagnosis.log 2>&1
echo "" >> test_diagnosis.log

echo "=== TESTE DE ENDPOINT DE PACIENTE ===" >> test_diagnosis.log
pytest tests/test_patients.py::TestPatientEndpoints::test_create_patient_success -v -s --tb=long >> test_diagnosis.log 2>&1
echo "" >> test_diagnosis.log

echo "=== RESUMO DE TODOS OS TESTES ===" >> test_diagnosis.log
pytest tests/ -v --tb=short >> test_diagnosis.log 2>&1

echo "Diagnóstico concluído. Verifique test_diagnosis.log"
