// Jenkins Pipeline for Playwright Tests
// 将此文件保存为 Jenkinsfile

pipeline {
    agent any

    environment {
        // Python 环境
        PYTHON_VERSION = 'python3.9'
        PIP_CACHE_DIR = "${WORKSPACE}/.cache/pip"

        // 测试环境变量（在 Jenkins Configure System 中设置）
        // TEST_URL = credentials('test-url')
        // TEST_USERNAME = credentials('test-username')
        // TEST_PASSWORD = credentials('test-password')
    }

    options {
        // 保留最近30天的构建记录
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
        // 超时时间60分钟
        timeout(time: 60, unit: 'MINUTES')
        // 禁止并发构建
        disableConcurrentBuilds()
    }

    stages {
        stage('准备环境') {
            steps {
                echo '准备测试环境...'
                sh '''
                    echo "工作目录: ${WORKSPACE}"
                    python3 --version || echo "Python3 未安装"
                    pip3 --version || echo "pip3 未安装"
                '''
            }
        }

        stage('安装依赖') {
            steps {
                echo '安装 Python 依赖和 Playwright 浏览器...'
                sh '''
                    # 升级 pip
                    python3 -m pip install --upgrade pip

                    # 安装 Python 依赖
                    pip3 install -r requirements.txt

                    # 安装 Playwright 浏览器
                    python3 -m playwright install --with-deps chromium
                '''
            }
        }

        stage('配置测试环境') {
            steps {
                echo '配置测试参数...'
                script {
                    if (env.TEST_URL) {
                        sh "sed -i 's|BASE_URL = \".*\"|BASE_URL = \\\"${env.TEST_URL}\\\"|g' test_login_advanced.py"
                    }
                    if (env.TEST_USERNAME) {
                        sh "sed -i 's/USERNAME = \".*\"/USERNAME = \\\"${env.TEST_USERNAME}\\\"/g' test_login_advanced.py"
                    }
                    if (env.TEST_PASSWORD) {
                        sh "sed -i 's/PASSWORD = \".*\"/PASSWORD = \\\"${env.TEST_PASSWORD}\\\"/g' test_login_advanced.py"
                    }
                }
            }
        }

        stage('运行测试') {
            steps {
                echo '执行 Playwright 自动化测试...'
                sh '''
                    # 运行测试
                    python3 -m pytest test_login_advanced.py \
                        -v \
                        --browser chromium \
                        --junitxml=test-results/junit.xml \
                        --html=test-report.html \
                        --self-contained-html \
                        || true
                '''
            }
        }

        stage('并行测试（可选）') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                echo '使用 pytest-xdist 并行运行测试...'
                sh '''
                    # 安装 pytest-xdist
                    pip3 install pytest-xdist

                    # 并行运行测试（使用所有可用的 CPU 核心）
                    python3 -m pytest test_login_advanced.py \
                        -v \
                        -n auto \
                        --browser chromium \
                        || true
                '''
            }
        }

        stage('生成测试报告') {
            steps {
                echo '生成测试报告...'
                sh '''
                    # JSON 报告已经由测试生成
                    # 可以添加额外的报告处理逻辑
                    echo "测试报告位置: ${WORKSPACE}/test_report.json"

                    # 如果安装了 json2html，生成 HTML 报告
                    # pip3 install json2html
                    # python3 -c "import json; from json2html import json2html; data = json.load(open('test_report.json')); open('test_report.html', 'w').write(json2html.convert(json=data))"
                '''
            }
        }

        stage('发布测试报告') {
            steps {
                // 发布 JUnit 测试报告
                junit testResults: 'test-results/*.xml', allowEmptyResults: true

                // 发布 HTML 报告
                publishHTML([
                    reportDir: '.',
                    reportFiles: 'test-report.html',
                    reportName: 'Playwright Test Report',
                    alwaysLinkToLastBuild: true,
                    keepAll: true
                ])

                // 归档测试报告
                archiveArtifacts artifacts: 'test_report.json,test-report.html,screenshots/**/*', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo '清理工作空间...'
            // 清理可选，根据需要决定是否保留
            // cleanWs()
        }

        success {
            echo '✅ 测试执行成功！'
            // 发送成功通知（可选）
            // slackSend(color: 'good', message: "Playwright 测试成功: ${env.JOB_NAME} - ${env.BUILD_NUMBER}")
        }

        failure {
            echo '❌ 测试执行失败！'
            // 发送失败通知（可选）
            // slackSend(color: 'danger', message: "Playwright 测试失败: ${env.JOB_NAME} - ${env.BUILD_NUMBER}")
        }

        unstable {
            echo '⚠️ 测试结果不稳定（有测试失败）！'
        }

        cleanup {
            // 发送邮件通知（可选）
            emailext(
                subject: "Playwright 测试报告: ${currentBuild.currentResult} - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Playwright 测试执行报告</h2>
                    <p><strong>项目:</strong> ${env.JOB_NAME}</p>
                    <p><strong>构建号:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>状态:</strong> ${currentBuild.currentResult}</p>
                    <p><strong>持续时间:</strong> ${currentBuild.durationString}</p>
                    <p><a href="${env.BUILD_URL}">查看详细日志</a></p>
                """,
                to: 'test-team@example.com',
                mimeType: 'text/html',
                attachLog: true
            )
        }
    }
}

// 多阶段 Pipeline 示例（如果需要在不同环境测试）
/*
def browsers = ['chromium', 'firefox', 'webkit']
browsers.each { browser ->
    stage("测试: ${browser}") {
        steps {
            sh """
                python3 -m pytest test_login_advanced.py \
                    -v \
                    --browser ${browser} \
                    --html=test-report-${browser}.html
            """
        }
    }
}
*/
