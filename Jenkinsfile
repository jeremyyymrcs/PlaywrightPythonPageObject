pipeline {
    agent {
        docker {
            image 'playwright-sample-project'  // Docker image
            args '-v /var/run/docker.sock:/var/run/docker.sock -v //c/ProgramData/Jenkins/.jenkins/workspace:/app'
        }
    }
    stages {
        stage('Start Container') {
            steps {
                script {
                    echo 'Starting the container...'

                    // Start the container if not running
                    def containerRunning = sh(script: 'docker ps -q -f name=friendly_wilson', returnStdout: true).trim()

                    if (!containerRunning) {
                        echo 'Container not running. Starting the container...'
                        // Start the container in detached mode (non-interactive)
                        sh 'docker run -d --name friendly_wilson playwright-sample-project'
                    } else {
                        echo 'Container is already running.'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests inside the container...'

                    // Run the test script inside the running container
                    sh 'docker exec friendly_wilson /bin/bash -c "/app/tests/scripts/run_test_suite.sh"'
                }
            }
        }

        stage('Archive Allure Results') {
            steps {
                script {
                    echo 'Archiving Allure Results...'
                    archiveArtifacts artifacts: 'reports/allure-report/**/*', allowEmptyArchive: true
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                script {
                    echo 'Publishing Allure Report in Jenkins...'
                    allure includeProperties: false, jdk: '', results: 'reports/allure-results'
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
