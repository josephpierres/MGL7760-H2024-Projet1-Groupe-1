pipeline {
  agent none
  stages {
    stage('Back-end') {
      agent {
        docker { image 'wsgi' }
      }
      steps {
        sh 'docker compose up'
      }
    }
    stage('Front-end') {
      agent {
        docker { image 'wsgi' }
      }
      steps {
        sh 'docker compose up'
      }
    }
  }
}
