pipeline {
    agent any

    environment {
        GCP_PROJECT = "precise-ascent-468019-a0"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage("Checkout repo") {
            steps {
                script {
                    echo "Checkout repo"
                    git config --global --add safe.directory "*"
                    ls -lah .
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token-august', name: 'HotelReservations', url: 'https://github.com/tanglisha/MLOps-Bootcamp-Hotel-Reservations.git']])
                }
            }
        }

        stage("Build & push image to GCP") {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo "Build & push image to GCP"
                        sh '''
                        export PATH=$PATH:"${GOOGLE_APPLICATION_CREDENTIALS}"
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet 
                        docker compose build app
                        docker push gcr.io/${GCP_PROJECT}/ml-bootcamp-hotel-reservations:latest
                        '''
                    }
                }   
            } // withCredentials
        } // steps
    } // build & push image to gcp
} // stages

// 1:06