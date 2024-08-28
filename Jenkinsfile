pipeline {
    agent {
        node {
            label params.SLAVE
        }
    }

    parameters{
        string(name: 'SLAVE', defaultValue: 'wano_slave')
        string(name: 'EO_GAS_URL', defaultValue: 'https://gas.massimo.hall149-x3.ews.gic.ericsson.se')
        string(name: 'EO_GAS_USERNAME', defaultValue: 'gas-user')
        string(name: 'EO_GAS_PASSWORD', defaultValue: 'Ericsson123!')
    }

    environment { /* horrible hack - needed until we access again to the Jenkins nodes configuration */
        bob2 = "PATH=${PATH}:/app/vbuild/RHEL7-x86_64/python/3.11.0/bin/ ./bob/bob"
        DOCKER_CREDS = credentials('armdocker-so-login')
        ARTIFACTORY_CREDS = credentials('artifactory-esoadm-login')
    }

    stages {
        stage('Add bob and config files') {
            steps {
                sh "uname -a"
                sh "git submodule add -f ssh://gerrit.ericsson.se:29418/adp-cicd/bob bob"
                sh "git submodule update --init --recursive"
                sh "git config submodule.bob.ignore all"
            }
        }

        stage('Clean') {
            steps {
                sh "${bob2} -lq"
            }
        }

        stage('Build') {
            steps {
                sh "${bob2} build"
            }
        }

        stage('Run') {
            steps {
                sh "${bob2} run"
            }
        }
    }
}
