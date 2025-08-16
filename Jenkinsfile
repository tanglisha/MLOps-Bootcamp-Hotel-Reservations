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
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', name: 'HotelReservations', url: 'https://github.com/tanglisha/MLOps-Bootcamp-Hotel-Reservations.git']])
                }
            } // steps
        } // stage: checkout repo

        stage("Build & push image to GCP") {
            steps {
                withCredentials([file(credentialsId: 'gcp-creds', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo "Build & push image to GCP"
                        sh '''
                        export PATH=$PATH:"${GOOGLE_APPLICATION_CREDENTIALS}"
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet 
                        docker build --secret id=GOOGLE_APPLICATION_CREDENTIALS,src=${GOOGLE_APPLICATION_CREDENTIALS} -t gcr.io/${GCP_PROJECT}/ml-bootcamp-hotel-reservations:latest . 
                        // docker compose build app
                        docker push gcr.io/${GCP_PROJECT}/ml-bootcamp-hotel-reservations:latest
                        '''
                        } // script
                } // withCredentials
            } // steps
        } // stage: build & push image to gcp

        stage("Deploy to Google Cloud Run") {
            steps {
                withCredentials([file(credentialsId: 'gcp-creds', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo "Deploy to Google Cloud Run"
                        sh '''
                        export PATH=$PATH:"${GOOGLE_APPLICATION_CREDENTIALS}"
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud run deploy ml-bootcamp-hotel-reservations \
                            --image=gcr.io/${GCP_PROJECT}/ml-bootcamp-hotel-reservations:latest \
                            --platform=managed \
                            --region=us-central-1 \
                            --allow-unauthenticated \
                            --set-env-vars PORT=8080
                        '''
                        } // script
                } // withCredentials
            } // steps
        } // stage: Deploy to Google Cloud Run
    } // stages
} // pipeline

// TODO: You've changed how secrets work, switch back to compose if you can't figure out 
// how to include them in vanilla docker build