pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                script {
                    // Initial setup, installation of dependencies
                    sh 'make setup'
                }
            }
        }

        stage('Static Analysis') {
            steps {
                script {
                    // Run static code analysis with Pylint and Flake8
                    sh 'make flake8'
                }
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    // Run unit tests and generate coverage report
                    sh 'make test-coverage'
                }
            }
        }

        stage('Generate Documentation') {
            steps {
                script {
                    // Generate documentation with pdoc
                    sh 'make docs'
                }
            }
        }

        stage('Quality Checks') {
            steps {
                script {
                    // Check code coverage against a minimum threshold
                    sh 'make test'
                }
            }
        }
    }

    post {
        always {
            // Archive generated reports for visualization in Jenkins
            archiveArtifacts artifacts: 'flake8_report.xml,coverage_report.xml,docs/**', fingerprint: true
        }
    }
}
