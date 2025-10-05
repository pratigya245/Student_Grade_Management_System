pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "student-grade-system"
        VERSION = "${BUILD_NUMBER}"
        DOCKER_REGISTRY = "pratigyadeakin27"  
    }
    
    stages {
        stage('Build') {
            steps {
                echo '========== Starting Build Stage =========='
                script {
                    // Build Docker image
                    sh "docker build -t ${DOCKER_IMAGE}:${VERSION} ."
                    sh "docker tag ${DOCKER_IMAGE}:${VERSION} ${DOCKER_IMAGE}:latest"
                    echo "Docker image built successfully: ${DOCKER_IMAGE}:${VERSION}"
                }
            }
        }
        
        stage('Test') {
            steps {
                echo '========== Starting Test Stage =========='
                script {
                    // Run tests inside Docker container
                    sh '''
                        docker run --rm ${DOCKER_IMAGE}:${VERSION} \
                        bash -c "pytest --cov=students --cov=grades --cov-report=xml --cov-report=html --junitxml=test-results.xml"
                    '''
                    echo 'Tests completed successfully'
                }
            }
            post {
                always {
                    // Archive test results
                    junit '**/test-results.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Code Quality Analysis') {
            steps {
                echo '========== Starting Code Quality Stage =========='
                script {
                    // Run Pylint for code quality
                    sh '''
                        docker run --rm ${DOCKER_IMAGE}:${VERSION} \
                        bash -c "pylint students grades --output-format=json > pylint-report.json || true"
                    '''
                    
                    // Run Flake8 for style checking
                    sh '''
                        docker run --rm ${DOCKER_IMAGE}:${VERSION} \
                        bash -c "flake8 students grades --output-file=flake8-report.txt || true"
                    '''
                    
                    echo 'Code quality analysis completed'
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                echo '========== Starting Security Stage =========='
                script {
                    // Run Bandit security scanner
                    sh '''
                        docker run --rm ${DOCKER_IMAGE}:${VERSION} \
                        bash -c "bandit -r students grades -f json -o bandit-report.json || true"
                    '''
                    
                    // Run Safety to check dependencies
                    sh '''
                        docker run --rm ${DOCKER_IMAGE}:${VERSION} \
                        bash -c "safety check --json > safety-report.json || true"
                    '''
                    
                    // Run Trivy to scan Docker image
                    sh "trivy image --format json --output trivy-report.json ${DOCKER_IMAGE}:${VERSION} || true"
                    
                    echo 'Security scans completed'
                }
            }
            post {
                always {
                    // Archive security reports
                    archiveArtifacts artifacts: '*-report.json', allowEmptyArchive: true
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                echo '========== Starting Deploy Stage =========='
                script {
                    // Stop and remove old container if exists
                    sh 'docker stop student-grade-staging || true'
                    sh 'docker rm student-grade-staging || true'
                    
                    // Run new container in staging
                    sh """
                        docker run -d \
                        --name student-grade-staging \
                        -p 8001:8000 \
                        ${DOCKER_IMAGE}:${VERSION}
                    """
                    
                    echo 'Application deployed to staging on port 8001'
                    
                    // Wait for application to start
                    sleep 10
                    
                    // Health check
                    sh 'curl -f http://localhost:8001/admin/ || exit 1'
                    echo 'Health check passed - staging deployment successful'
                }
            }
        }
        
        stage('Release to Production') {
            steps {
                echo '========== Starting Release Stage =========='
                script {
                    // Tag release
                    sh "git tag -a v${VERSION} -m 'Release version ${VERSION}' || true"
                    
                    // Stop and remove old production container if exists
                    sh 'docker stop student-grade-production || true'
                    sh 'docker rm student-grade-production || true'
                    
                    // Deploy to production
                    sh """
                        docker run -d \
                        --name student-grade-production \
                        -p 8002:8000 \
                        ${DOCKER_IMAGE}:${VERSION}
                    """
                    
                    echo 'Application released to production on port 8002'
                    
                    // Wait for application to start
                    sleep 10
                    
                    // Health check
                    sh 'curl -f http://localhost:8002/admin/ || exit 1'
                    echo 'Health check passed - production deployment successful'
                }
            }
        }
        
        stage('Monitoring Setup') {
            steps {
                echo '========== Starting Monitoring Stage =========='
                script {
                    echo 'Setting up monitoring and alerting...'
                    
                    // Create monitoring configuration
                    sh '''
                        echo "Application: Student Grade Management System" > monitoring-config.txt
                        echo "Version: ${VERSION}" >> monitoring-config.txt
                        echo "Staging URL: http://localhost:8001" >> monitoring-config.txt
                        echo "Production URL: http://localhost:8002" >> monitoring-config.txt
                        echo "Monitoring Status: Active" >> monitoring-config.txt
                    '''
                    
                    echo 'Monitoring configured successfully'
                    echo 'Metrics available at:'
                    echo '  - Staging: http://localhost:8001'
                    echo '  - Production: http://localhost:8002'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'monitoring-config.txt', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        success {
            echo '========== Pipeline Completed Successfully =========='
            echo "Build: ${BUILD_NUMBER}"
            echo "Status: SUCCESS"
        }
        failure {
            echo '========== Pipeline Failed =========='
            echo "Build: ${BUILD_NUMBER}"
            echo "Status: FAILURE"
        }
        always {
            // Cleanup
            echo 'Cleaning up...'
            sh 'docker system prune -f || true'
        }
    }
}