pipeline {
    agent any

    triggers {
    // Trigger the pipeline when a push is made to the 'main' branch
    gitHubPush()
    }


    environment {
        // Define the Docker container image you're using
        DOCKER_IMAGE = 'playwright-sample-project'  // Replace with your Docker image name
        CONTAINER_NAME = 'friendly_wilson'         // Name of your pre-existing container
        ALLURE_RESULTS_DIR = 'allure-results'      // Directory where Allure stores the results
        ALLURE_REPORT_DIR = '/app/reports/allure-report'       // Directory to store the generated Allure report
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
                ansiColor('xterm') {  // Apply ANSI color support
                    script {
                        // Start your pre-existing Docker container if not already running
                        def containerRunning = bat(script: "docker ps -q -f name=${CONTAINER_NAME}", returnStdout: true).trim()

                        if (!containerRunning) {
                            // If the container is not running, start it
                            echo "Starting container ${CONTAINER_NAME}"
                            // You can use docker start if it exists or docker run to create a new container if needed
                            bat "docker start ${CONTAINER_NAME} || docker run -d --name ${CONTAINER_NAME} ${DOCKER_IMAGE}"
                        } else {
                            echo "Container ${CONTAINER_NAME} is already running"
                        }

                        // Run the test script inside the container and generate the Allure report
                        echo "Running Playwright tests inside the container"
                        bat "docker exec ${CONTAINER_NAME} ./run_test_suite.sh"
                    }
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                script {
                    echo "Copying Allure report from container to Jenkins workspace"
                    // Copy the Allure report directory from the container to the workspace
                    bat "docker cp ${CONTAINER_NAME}:${ALLURE_REPORT_DIR} ${WORKSPACE}/allure-report"
                }
            }
        }
    }

    post {
        always {
            // Clean workspace or perform any necessary post-build actions
            cleanWs()
        }
    }
}



