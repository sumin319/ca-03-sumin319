pipeline {
    agent { docker { image 'shahatuh/dp2306' } }

    environment {
        PATH = "env/bin/:$PATH"
    }
    stages {
        stage('build') {
            steps {
                sh 'python ca_03.py -i Images/hubble.ppm -t 120 -b 15 -m Stack -d 0'
                sh 'python ca_03.py -i Images/hubble.ppm -t 120 -b 15 -m Queue -d 0'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'output/**/*.* ', onlyIfSuccessful: true
        }
    }
}
