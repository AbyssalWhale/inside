# Enviroment Requrements
- [Python](https://www.python.org/downloads/)
- [PIP](https://pypi.org/project/pip/)
- [Pycharm](https://www.jetbrains.com/pycharm/)
- packages from ```requirements.txt```
- [playwright](https://playwright.dev/python/docs/intro)

# High-Level Structure
```
├── .github - github action wrokflows
├── configs - mostly K8S. Good idea to move dockerfiles here as well
├── enums - project enums grouped by category: playwright, sut (system under test), tests_enum. 
├── helpers - helpers that are used interact with browser, system and test-run-config.json
├── models - project models grouped by category: api, poms (Page Object Models) etc
├── tests - all project tests
├── .gitignore - list of ignored items by git
├── conftest.py - fixtures
├── controller.py - controller pod file. It deploys runner and trigger test executions on tunner pods
├── runner.py - runner. Accepts requests from controller regarding tests data and then execute tests
├── Dockerfile - dockerfile for tests-runner (aka python-tests:latest). It also used here in GitHub actions to run tests;
├── Dockerfile_TC - dockerfile for controller (aka tests-controller:latest). It also used here in GitHub actions to run tests;
├── pytest.ini - pytest configuration file
├── README.md - readme file 
├── requirements.txt - required packages 
└── test-run-config.json - test run config file that is used during test execution. Contains: URL, credentials, keys etc.
```
# Local Setup
1. Install minikube
2. run to set your Docker environment to point to Minikube’s Docker daemon: eval $(minikube docker-env) 
3. build controller: ``` docker build -f Dockerfile_TC -t tests-controller:latest . ```
4. build test-executor: ``` docker build -t python-tests . ```
5. we need to have cluster role which allow controller to manage services in cluster 
6. run command: ``` kubectl apply -f configs/k8s/minik/default/deployment/test_runner_clusterrole.yaml ```
7. run command: ``` kubectl apply -f configs/k8s/minik/default/deployment/test_runner_clusterrolebinding.yaml ```
8. create controller deployment. Run: ``` kubectl apply -f test_controller_d.yaml ```
9. it will update ```replicas``` in ``` tests_runner_d.yaml ``` -> try to deploy then
10. send ```POST``` request to execute test cases. if response is not ```200``` - it will retry (5 times max)
11. check deployment and pods. Deployments: 2, pods: 1 controller + 5 runners
12. Give some time. Around 20 seconds. Check logs of runners and controller. It should have info regarding test execution
13. copy tests result from pod: kubectl cp pod:/app/tests-results/junit-test-results.xml ./junit-test-results.xml
14. there are also conf files to deploy pods manually without deployment. 
![image](https://github.com/user-attachments/assets/661b1633-0559-4af7-9a1b-af8ea4aa585c)
![image](https://github.com/user-attachments/assets/44ab2577-b3bd-4a97-bd68-bc6013f11b1f)
![image](https://github.com/user-attachments/assets/965d7f19-8015-4615-9584-d6de9cfd97d6)
![image](https://github.com/user-attachments/assets/36cb3d4a-26dd-4165-94f4-a8e9e4500ec5)

# AWS ECS
- build and push happen from GitHub Actions piepline. Please check it out
# AWS EKS
- created cluster
- set connection between EC2 and EKS cluster
- failed to create node group and as result my pod deployment just stuck. Maybe issues with Role policies that is used for Node Group or VPC. Still figuring it out.
![image](https://github.com/user-attachments/assets/eaccf718-f3ce-4ff4-b905-64daa25abfaa)
![image](https://github.com/user-attachments/assets/e41abe28-ecd2-403b-9a2a-2caea4b86214)
![image](https://github.com/user-attachments/assets/18280f37-2bf8-43e8-9825-9da542dc1b2b)
![image](https://github.com/user-attachments/assets/42f5bc71-27f1-4767-98a1-04097c842664)











