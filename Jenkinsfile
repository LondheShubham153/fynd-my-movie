def COLOR_MAP = [
    'SUCCESS': 'good', 
    'FAILURE': 'danger',
]

pipeline {
    agent { label 'ZorinOS' }

    environment {
        PYTHON_VERSION = "3"
        registryCredential = "Dockerhub_creads"
        registry = "https://index.docker.io/v1/"
        appRegistry = "dineshtamang14/movies-api"
        SONARSERVER = 'sonarserver'
        SONARSCANNER = 'sonarscanner'
    }

    stages {
        stage("Installing dependencies"){
            steps {
                sh "pip3 install -r requirements.txt"
            }
        }
        
        stage('SonarQube Analysis') {
            environment {
                scannerHome = tool "${SONARSCANNER}"
            }
            steps {
               withSonarQubeEnv("${SONARSERVER}") {
		sh "${scannerHome}/bin/sonar-scanner"
              }
            }
        }
        
        stage("Quality Gate") {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
                    // true = set pipeline to UNSTABLE, false = don't
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage("Build"){
            steps {
                script {
                    dockerImage = docker.build(appRegistry + ":$BUILD_NUMBER", ".")
                }
            }
        }
        
        stage('Push Docker image to Docker Hub') {
            steps {
                script {
                    docker.withRegistry(registry, registryCredential){
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy Docker container to remote server') {
            steps {
                sh "docker run -itd -p 5000:8000 dineshtamang14/movies-api:$BUILD_NUMBER"
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
