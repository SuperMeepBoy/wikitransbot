pipeline {

    agent {
        docker {
            image 'python:3.8.12-buster'
        }
    }
    environment {
        CI = 'true'
    }

    stages {
        stage("test") {
            steps {
                sh "python --version"
                sh "pip install -r requirements.txt"
                sh "flake8"
            }
        }
    }
}
