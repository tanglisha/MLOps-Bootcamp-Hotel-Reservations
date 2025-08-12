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
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/tanglisha/MLOps-Bootcamp-Hotel-Reservations.git']])
                }
            }
        }

        stage("Build & push image to GCP") {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIAL')]){
                    script{
                        echo "Build & push image to GCP"
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIAL}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet 
                        docker build -t gcr.io/${GCP_PROJECT}/ml-bootcamp-hotel-reservations:latest .
                        docker push gcr.io/${GCP_PROJECT}/ml-bootcamp-hotel-reservations:latest
                        '''
                    }
                }   
            } // withCredentials
        } // steps
    } // build & push image to gcp
} // stages