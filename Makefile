## ========== 开发时命令 ==============
redis-up: ## redis
	docker-compose -f develop.yml up -d redis

celery-run:
	celery worker -A mificloud.celery_app.app -l info -P eventlet


## ========== 测试与代码质量 ==============

test:
	@echo "--> Testing python"
	python -m py.test
	@echo ""


lint: ## check style with black
	@echo "--> Linting python"
	black .
	@echo ""

sort: # sort import with isort
	@echo "--> Sort python imort"
	isort -rc .
	@echo ""

## ========== 文件清理相关 ==============

clean: clean-build clean-pyc clean-test clean-pip ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	@echo "--> Cleaning build artifacts"
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +
	@echo ""

clean-pyc: ## remove Python file artifacts
	@echo "--> Cleaning pyc"
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	@echo ""

clean-test: ## remove test and coverage artifacts
	@echo "--> Cleaning test"
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	@echo ""


clean-pip:
	@echo "--> Cleaning pip wheel"
	rm -rf pip-wheel-metadata/
	@echo ""
