pipeline {
    agent any

    environment {
        // Define the Docker container image you're using
        DOCKER_IMAGE = 'playwright-sample-project'  // Replace with your Docker image name
        CONTAINER_NAME = 'friendly_wilson'         // Name of your pre-existing container
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your repository
                checkout scm
            }
        }

        stage('Run Playwright Tests') {
            steps {
                script {
                    // Start your pre-existing Docker container if not already running
                    def containerRunning = bat(script: "docker ps -q -f name=${CONTAINER_NAME}", returnStdout: true).trim()

                    if (!containerRunning) {
                        // If the container is not running, start it
                        echo "Starting container ${CONTAINER_NAME}"
                        bat "docker start -i ${CONTAINER_NAME}"
                    } else {
                        echo "Container ${CONTAINER_NAME} is already running"
                    }

                    // Run the test script inside the container
                    echo "Running Playwright tests inside the container"
                    bat "docker exec ${CONTAINER_NAME} ./run_test_suite.sh"
                }
            }
        }
    }


    post {
        success {
            // Archive the Allure report
            echo "Archiving Allure report"
            archiveArtifacts allowEmptyArchive: true, artifacts: 'allure-report/**', fingerprint: true

            // Clean up the generated Allure report from the workspace
            echo "Cleaning up Allure report from the workspace"
            sh "rm -rf allure-report/"
        }

        always {
            // Clean workspace after the build, excluding the allure-report directory
            cleanWs notFailBuild: true, deleteDirs: true, excludes: '**/allure-report/**'
        }
    }
}
