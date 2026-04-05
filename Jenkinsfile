pipeline {
    agent any

    environment {
        IMAGE_NAME = "prabhat2025/devops-ml-app"
        TAG = "${BUILD_NUMBER}"
        KUBECONFIG = 'C:\\Users\\prabh\\.kube\\config' 
        DEPLOYMENT_NAME = "devops-ml-app"
        CONTAINER_NAME = "devops-ml"
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

        stage('Deploy to Kind Cluster') {
            steps {
                bat """
                kubectl set image deployment/%DEPLOYMENT_NAME% %CONTAINER_NAME%=%IMAGE_NAME%:%TAG%
                kubectl rollout status deployment/%DEPLOYMENT_NAME%
                """
            }
        }
    }

    post {
        success {
            echo "✅ Docker image pushed and Kind deployment updated successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
