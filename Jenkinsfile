pipeline {
    agent none
    stages {
        stage('Start Container') {
            agent {
                docker {
                    image 'playwright-sample-project'
                    args '-u root:root'
                }
            }
            steps {
                script {
                    echo 'Starting the container...'
                    sh 'docker run -d --name friendly_wilson playwright-sample-project'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests inside the container...'
                    sh 'docker exec friendly_wilson /app/tests/scripts/run_test_suite.sh'
                }
            }
        }

        stage('Archive Results') {
            steps {
                script {
                    echo 'Archiving results...'
                    archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    echo 'Cleaning up the container...'
                    sh 'docker stop friendly_wilson && docker rm friendly_wilson'
                }
            }
        }
    }
}
