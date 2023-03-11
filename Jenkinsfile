def COLOR_MAP = [
    'SUCCESS': 'good', 
    'FAILURE': 'danger',
]

pipeline {
    agent { label 'ZorinOS' }

    environment {
        PYTHON_VERSION = '3'
        registryCredential = 'Dockerhub_creads'
        appRegistry = "docker.io/dineshtamang14/movies-api"
    }

    stages {
        stage("Installing dependencies"){
            steps {
                sh "pip3 install -r requirements.txt"
            }
        }
        
        stage("Build"){
            steps {
                script {
                    def dockerImage = docker.build(appRegistry + ":$BUILD_NUMBER", ".")
                    def dockerImageLatest = docker.image(appRegistry + ":$BUILD_NUMBER")
                    dockerImageLatest.tag(appRegistry + ":latest")
                }
            }
        }
        
        stage('Push Docker image to Docker Hub') {
            steps {
                script {
                    docker.withRegistry(vprofileRegistry, registryCredential){
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
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

    post {
        always {
            echo 'Slack Notifications.'
            slackSend channel: '#cicd-jenkins',
                color: COLOR_MAP[currentBuild.currentResult],
                message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
        }
    }
}