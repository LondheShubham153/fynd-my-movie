pipeline {
    agent any 

    environment {
        PYTHON_VERSION = '3.8.10'
    }

    stages {
        stage("Installing dependencies"){
            steps {
                sh "python${PYTHON_VERSION} -m venv env"
                sh "source env/bin/activate && pip3 install -r requirements.txt"
            }
        }

        stage("Unit Testing"){
            stpes {
                sh "source env/bin/activate && pytest"
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

        stage("Deploy"){
            steps {
                sh 'docker run -itd -p 8080:8000 --name movies-api dineshtamanag14/movies-api:$BUILD_NUMBER'
            }
        }
    }
    when {
       expression { branch == 'main' }
    }
}
