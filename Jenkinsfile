pipeline {
    agent any

    environment {
        IMAGE_NAME = "prabhat2025/devops-ml-app"
        TAG = "5"
    }

    stages {

        stage('Clone Code') {
            steps {
                git branch: 'main', url: 'https://github.com/DevOps-Fusion/MLOPS_Projects.git'
            }
        }

        stage('Install Dependencies & Train Model') {
            steps {
                bat '''
                pip install -r requirements.txt
                cd model
                python train.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%TAG% .'
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USERNAME',
                    passwordVariable: 'PASSWORD'
                )]) {
                    bat 'echo %PASSWORD% | docker login -u %USERNAME% --password-stdin'
                }
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                bat 'docker push %IMAGE_NAME%:%TAG%'
            }
        }
    }
}
