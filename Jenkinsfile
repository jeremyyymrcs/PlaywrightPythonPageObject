pipeline {
    agent any

    environment {
        // Define the Docker container image you're using
        DOCKER_IMAGE = 'playwright-sample-project'  // Replace with your Docker image name
        CONTAINER_NAME = 'friendly_wilson'         // Name of your pre-existing container
        ALLURE_RESULTS_DIR = 'allure-results'      // Directory where Allure stores the results
        ALLURE_REPORT_DIR = '/app/reports/allure-report' // Directory to store the generated Allure report
        LOCAL_ALLURE_REPORT_DIR = "${WORKSPACE}/allure-report" // Local directory in Jenkins workspace
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

                    // Run the test script inside the container and generate the Allure report
                    echo "Running Playwright tests inside the container"
                    bat "docker exec ${CONTAINER_NAME} ./run_test_suite.sh"
                }
            }
        }

        stage('Clean Up Old Allure Reports') {
            steps {
                script {
                    // Delete the previous Allure report if it exists in the workspace
                    echo "Cleaning up old Allure report in the workspace"
                    deleteDir("${LOCAL_ALLURE_REPORT_DIR}")  // Deletes the entire directory
                }
            }
        }

        stage('Copy Allure Report from Docker') {
            steps {
                script {
                    // Copy the generated Allure report from the Docker container to the Jenkins workspace
                    echo "Copying Allure report from Docker container to Jenkins workspace"
                    bat "docker cp ${CONTAINER_NAME}:${ALLURE_REPORT_DIR} ${LOCAL_ALLURE_REPORT_DIR}"
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                script {
                    // Ensure Allure results are found
                    echo "Checking if Allure report exists in ${LOCAL_ALLURE_REPORT_DIR}"
                    if (fileExists("${LOCAL_ALLURE_REPORT_DIR}/**/*")) {
                        echo "Allure report found!"
                        allure includeProperties: false, jdk: '', results: [[path: "${LOCAL_ALLURE_REPORT_DIR}"]]
                    } else {
                        echo "Allure report not found!"
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean workspace or perform any necessary post-build actions
            echo "Performing cleanup..."
            cleanWs() // Clean workspace if necessary (removes all files, including reports)
        }
    }
}

// pipeline {
//     agent any
//
//     environment {
//         // Define the Docker container image you're using
//         DOCKER_IMAGE = 'playwright-sample-project'  // Replace with your Docker image name
//         CONTAINER_NAME = 'friendly_wilson'         // Name of your pre-existing container
//         ALLURE_RESULTS_DIR = 'allure-results'      // Directory where Allure stores the results
//         ALLURE_REPORT_DIR = '/app/reports/allure-report'       // Directory to store the generated Allure report
//     }
//
//     stages {
//         stage('Checkout') {
//             steps {
//                 // Checkout the code from your repository
//                 checkout scm
//             }
//         }
//
//         stage('Run Playwright Tests') {
//             steps {
//                 script {
//                     // Start your pre-existing Docker container if not already running
//                     def containerRunning = bat(script: "docker ps -q -f name=${CONTAINER_NAME}", returnStdout: true).trim()
//
//                     if (!containerRunning) {
//                         // If the container is not running, start it
//                         echo "Starting container ${CONTAINER_NAME}"
//                         bat "docker start -i ${CONTAINER_NAME}"
//                     } else {
//                         echo "Container ${CONTAINER_NAME} is already running"
//                     }
//
//                     // Run the test script inside the container and generate the Allure report
//                     echo "Running Playwright tests inside the container"
//                     bat "docker exec ${CONTAINER_NAME} ./run_test_suite.sh"
//
//                 }
//             }
//         }
//
//         stage('Publish Allure Report') {
//             steps {
//                 script {
//                     // Ensure Allure results are found
//                     echo "Checking if Allure report exists in ${WORKSPACE}/${ALLURE_REPORT_DIR}"
//                     if (fileExists("${ALLURE_REPORT_DIR}/**/*")) {
//                         echo "Allure report found!"
//                         allure includeProperties: false, jdk: '', results: [[path: "${WORKSPACE}/${ALLURE_REPORT_DIR}"]]
//                     } else {
//                         echo "Allure report not found!"
//                     }
//                 }
//             }
//         }
//     }
//
//     post {
//         always {
//             // Clean workspace or perform any necessary post-build actions
//             cleanWs()
//         }
//     }
// }


