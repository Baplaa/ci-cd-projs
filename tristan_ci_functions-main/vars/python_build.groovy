def call(dockerRepoName, imageName, portNum) {
    pipeline {
        agent any

        parameters {
            booleanParam(defaultValue: false, description: 'Deploy the Service?', name: 'DEPLOY')
        }

        stages {
            stage('Build') {
                steps {
                    sh "pip3 install -r ./${dockerRepoName}/ci/requirements.txt --break-system-packages"
                }
            }
            stage('Lint') {
                steps {
                    sh "pylint --fail-under=5 ./${dockerRepoName}/*.py"
                }
            }
            stage('Security') {
                steps {
                    sh "/var/jenkins_home/.local/bin/safety check -r ./${dockerRepoName}/ci/requirements.txt"
                }
            }
            stage("Package") {
                when {
                    expression { env.GIT_BRANCH == 'origin/main' }
                }
                steps {
                    dir(dockerRepoName) {
                        withCredentials([string(credentialsId: 'Dockerhub', variable: 'TOKEN')]) {
                            sh "docker login -u REDACTED -p '$TOKEN' docker.io"
                            sh "docker build -t ${dockerRepoName}:latest --tag REDACTED/${dockerRepoName}:${imageName} ."
                            sh "docker push REDACTED/${dockerRepoName}:${imageName}"
                        }
                    }
                }
            }
            stage('Deploy') {
                when {
                    expression { params.DEPLOY }
                }
                steps {
                    withCredentials([string(credentialsId: 'Dockerhub', variable: 'TOKEN')]) {
                        sshagent(credentials: ['896b1b95-d7b7-4dab-aa56-b85756ddd353']) {
                            sh "ssh -o StrictHostKeyChecking=no azureuser@tristanlab6.westus.cloudapp.azure.com \"docker login -u REDACTED -p '${TOKEN}' docker.io && cd lab7/deployment && docker-compose pull && docker-compose up -d\""   
                        }
                    }
                }
            }
        }
    }
}
