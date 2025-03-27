pipeline {
    agent none  // Don't use the default docker agent for the entire pipeline
    stages {
        stage('Start Container') {
            agent {
                docker {
                    image 'playwright-sample-project'  // Your custom image
                    // Use Linux-style path for Docker on Windows
                    args '-v /var/run/docker.sock:/var/run/docker.sock -v /c/ProgramData/Jenkins/.jenkins/workspace:/app'
                }
            }
            steps {
                script {
                    echo 'Starting the container and running tests...'
                    // Docker inside step to start container and run tests in one go
                    sh 'docker run -d --name friendly_wilson playwright-sample-project'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests inside the container...'
                    // Run the test script inside the running container
                    sh 'docker exec friendly_wilson /app/tests/scripts/run_test_suite.sh'
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
