pipeline {
    agent any

    stages {

        stage('Analyse static') {
            steps {
                script {
                    // Run unit tests and generate coverage report
                    sh 'echo adadad | sudo -S make analysis'
                }
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    // Run unit tests and generate coverage report
                    sh 'echo adadad | sudo -S make test'
                }
            }
        }

        stage('Generate Documentation') {
            steps {
                script {
                    // Generate documentation with pdoc
                    sh 'echo adadad | sudo -S make docs'
                }
            }
        }

        stage('Coverage Check') {
            steps {
                script {
                    // Check code coverage against a minimum threshold
                    sh 'echo adadad | sudo -S make coverage'
                }
            }
        }
    }

    post {
        always {
            // Archive generated reports for visualization in Jenkins
            archiveArtifacts artifacts: 'flake8_report.xml,test_results.xml,coverage.xml,docs.xml,docs/**', fingerprint: true
        }
    }
}