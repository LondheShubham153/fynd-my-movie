pipeline {
    agent { label 'ZorinOS' }

    environment {
        PYTHON_VERSION = '3'
    }

    stages {
        stage("Installing dependencies"){
            steps {
                sh "pip3 install -r requirements.txt"
            }
        }

        stage("Unit Testing"){
            steps {
                sh "pytest"
            }
        }
        
        stage("Build"){
            steps {
                script {
                    def dockerImage = docker.build('dineshtamang14/movies-api:$BUILD_NUMBER')
                    def dockerImageLatest = docker.image('dineshtamang14/movies-api:$BUILD_NUMBER')
                    dockerImageLatest.tag("dineshtamang14/movies-api:latest")
                }
            }
        }
        
        stage('Authenticate with Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        }
                    }
                }
            }
        }
        stage('Push Docker image to Docker Hub') {
            steps {
                script {
                    def dockerImage = docker.load("dineshtamang14/movies-api:$BUILD_NUMBER")
                    dockerImage.push()
                    def dockerImageLatest = docker.load("dineshtamang14/movies-api:latest")
                    dockerImageLatest.push()
                }
            }
        }

        stage('Deploy Docker container to remote server') {
            steps {
                script {
                    sshCommand remote: '$remote-server', user: '$username', password: '$password', command: """
                        docker run -d -p 8000:8000 --name movies-api dineshtamang14/movies-api:$BUILD_NUMBER
                    """
                }
            }
        }
    }
}
