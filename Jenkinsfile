pipeline {
    agent any 

    environment {
        PYTHON_VERSION = '3.8.0'
    }

    stages {
        stage("Clone Repo"){
            git branch: 'main', url: 'https://github.com/dineshtamang14/fynd-my-movie.git'
        }

        stage("Installing dependencies"){
            steps {
                sh "python${PYTHON_VERSION} -m venv env"
                sh "source env/bin/activate && pip install -r requirements.txt"
            }
        }

        stage("Unit Testing"){
            stpes {
                sh "source env/bin/activate && pytest"
            }
        }

        stage("Deploy"){
            steps {
                sh 'source env/bin/activate && python app.py'
            }
        }
    }
}