pipeline {
    agent any
    stages {
        stage('Test') {
            agent {
                dockerfile {
                    args '-u root:root'
                    reuseNode true
                }
            }
            steps {
                sh "behave -D record_mode=none --tags=-skip -f json.cucumber -o test-results.json"
            }
        }
    }
    post {
        always {
            cucumber 'test-results.json'
        }
    }
}
