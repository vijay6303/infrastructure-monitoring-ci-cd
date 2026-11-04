pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r monitoring/requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m unittest discover -s tests -v
                '''
            }
        }

        stage('Run Monitoring') {
            steps {
                sh '''
                    . venv/bin/activate
                    python monitoring/monitor.py
                '''
            }
        }

    }

    post {
        success {
            echo 'Infrastructure monitoring pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
