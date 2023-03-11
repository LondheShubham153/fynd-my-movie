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
                sh "docker build -t dineshtamang14/movies-api:$BUILD_NUMBER"
                sh "docker tag dineshtamang14/movies-api:$BUILD_NUMBER dineshtamang14/movies-api:latest"
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
