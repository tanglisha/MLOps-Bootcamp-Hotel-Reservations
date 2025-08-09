pipeline {
    agent any
    stages {
        stage("Checkout repo") {
            steps {
                script {
                    echo "Checkout repo"
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/tanglisha/MLOps-Bootcamp-Hotel-Reservations.git']])
                }
            }
        }
    }
}

