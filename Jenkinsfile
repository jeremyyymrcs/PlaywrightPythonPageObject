pipeline {
    agent {
        docker {
            image 'playwright-sample-project'  // Use your custom Docker image
            label 'docker'                    // Optional: specify a specific agent label
            args '-v /var/run/docker.sock:/var/run/docker.sock -v $WORKSPACE:/app' // Mount Jenkins workspace into the container
        }
    }
    environment {
        // Add any environment variables if necessary
    }
    stages {
        stage('Checkout') {
            steps {
                // Checkout the code repository (from SCM)
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run the test suite inside the Docker container
                    docker.start('friendly_wilson')
                    echo 'Running tests inside the container...'

                    // Execute the test script that generates the Allure report
                    sh 'docker exec friendly_wilson /bin/bash -c "/app/tests/scripts/run_test_suite.sh"'
                }
            }
        }

        stage('Archive Allure Results') {
            steps {
                script {
                    // Archive the Allure results directory as a build artifact
                    echo 'Archiving Allure Results...'
                    // Archive the Allure results directory generated inside the container
                    archiveArtifacts artifacts: 'reports/allure-report/**/*', allowEmptyArchive: true
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                script {
                    // Use Allure Jenkins Plugin to display the Allure report directly in Jenkins
                    echo 'Publishing Allure Report in Jenkins...'
                    allure includeProperties: false, jdk: '', results: 'reports/allure-results'
                }
            }
        }

    post {
        always {
            // Cleanup after the build
            echo 'Cleaning up...'
        }

        success {
            echo 'Tests executed successfully!'
        }

        failure {
            echo 'Tests failed. Please check logs for details.'
        }
    }
}
