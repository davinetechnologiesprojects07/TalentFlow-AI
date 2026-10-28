pipeline {
    agent any

    environment {
        IMAGE_NAME    = 'ironman41732029/talentflow-ai'
        IMAGE_TAG     = "${env.BUILD_NUMBER}"
        DOCKER_CONFIG = "${env.WORKSPACE}\\.docker"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/sumanth-p25/TalentFlow-AI.git'
            }
        }

        stage('Check Tools') {
            steps {
                bat 'git --version'
                bat 'docker --version'
                bat 'docker compose version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
                bat 'docker tag %IMAGE_NAME%:%IMAGE_TAG% %IMAGE_NAME%:latest'
            }
        }

        stage('Trivy Security Scan') {
            steps {
                bat '''
                docker run --rm ^
                  -v "%WORKSPACE%:/work" ^
                  -v trivy-cache:/root/.cache ^
                  -w /work ^
                  aquasec/trivy:0.75.0 ^
                  fs --scanners vuln,misconfig,secret ^
                  --severity HIGH,CRITICAL ^
                  --exit-code 1 ^
                  --no-progress --skip-version-check .
                '''
            }
        }

        stage('Push to Docker Hub') {
            environment {
                // Only the credential ID goes here. Creates DOCKERHUB_CREDS_USR / _PSW.
                DOCKERHUB_CREDS = credentials('dockerhub-creds')
            }
            steps {
                bat '''
                @echo off

                echo ===== DIAGNOSTICS =====
                echo Jenkins credential username : %DOCKERHUB_CREDS_USR%
                echo Image to push               : %IMAGE_NAME%:%IMAGE_TAG%

                if "%DOCKERHUB_CREDS_USR%"=="" (
                    echo ERROR: username is empty - credential kind must be "Username with password"
                    exit /b 1
                )
                if "%DOCKERHUB_CREDS_PSW%"=="" (
                    echo ERROR: token is empty
                    exit /b 1
                )
                echo =======================

                echo %DOCKERHUB_CREDS_PSW%| docker login -u %DOCKERHUB_CREDS_USR% --password-stdin
                if errorlevel 1 exit /b 1

                docker push --quiet %IMAGE_NAME%:%IMAGE_TAG%
                if errorlevel 1 exit /b 1
                docker push --quiet %IMAGE_NAME%:latest
                if errorlevel 1 exit /b 1
                '''
            }
            post {
                always { bat 'docker logout || exit /b 0' }
            }
        }

        stage('Deploy to Kubernetes') {
            // Skipped (not failed) if your repo has no k8s folder
            when { expression { fileExists('k8s') } }
            steps {
                bat 'kubectl apply -f k8s/'
                bat 'kubectl set image deployment/talentflow-ai talentflow-ai=%IMAGE_NAME%:%IMAGE_TAG%'
                bat 'kubectl rollout status deployment/talentflow-ai --timeout=120s'
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded.' }
        failure { echo 'Pipeline failed. Check the stage logs.' }
    }
}