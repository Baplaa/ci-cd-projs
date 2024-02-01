def call(dockerRepoName, imageName, portNum) {
    pipeline {
	agent any

     parameters {
        booleanParam(defaultValue: false, description: 'Deploy the App', name: 'DEPLOY')
    }

	stages {
		stage('Build') {
			steps {
				sh 'pip install -r ./ci/requirements.txt --break-system-packages'
				sh 'pip install --upgrade flask --break-system-packages'
			
			}
		}

		stage('Python Lint') {
			steps {
				sh 'pylint --fail-under=5 *.py'
			}
		}

		stage('Test and Coverage') {
            steps {
                script {
                    // Remove any existing test results
                    sh 'rm -f test-reports/*.xml || true'
                    sh 'rm -f api-test-reports/*.xml || true'
                    sh 'rm -f car-test-reports/*.xml || true'
                    
                    // Get all test files
                    def testFiles = findFiles(glob: 'test*.py')
                    
                    // Run tests with coverage for each test file
                    testFiles.each {
                        sh "coverage run --omit */site-packages/*,*/dist-packages/* ${it}"
                    }
                }
            }
            post {
                always {
                    sh 'coverage report'
                    
                    // Process the test results if they exist
                    script {
                        def test_reports_exist = fileExists 'test-reports'
                        if (test_reports_exist) {
                            junit 'test-reports/*.xml'
                        }
                        def api_test_reports_exist = fileExists 'api-test-reports'
                        if (api_test_reports_exist) {
                            junit 'api-test-reports/*.xml'
                        }
                        def car_test_reports_exist = fileExists 'car-test-reports'
                        if (car_test_reports_exist) {
                            junit 'car-test-reports/*.xml'
                        }
                    }
                }
            }
		}

        stage('Package') {
            when {
                expression { env.GIT_BRANCH == 'origin/main' }
            }
            steps {
                withCredentials([string(credentialsId: 'Dockerhub', variable: 'TOKEN')]) {
                    sh "docker login -u REDACTED -p '$TOKEN' docker.io"
                    sh "docker build -t ${dockerRepoName}:latest --tag REDACTED/${dockerRepoName}:${imageName} ."
                    sh "docker push REDACTED/${dockerRepoName}:${imageName}"
                }
            }
        }

		stage('Zip Artifacts') {
			steps {
				// Zip all .py files
                sh 'zip app.zip *.py'
                
                // Archive the zip file
                archiveArtifacts artifacts: 'app.zip', fingerprint: true
			}
		}

        stage("Deliver") {  
                when {
                    expression { params.DEPLOY }
                }
                steps {
                    sh "docker stop ${dockerRepoName} || true && docker rm ${dockerRepoName} || true"
                    sh "docker run -d -p ${portNum}:${portNum} --name ${dockerRepoName} ${dockerRepoName}:latest"
                }
            }
	    }
    }
}
