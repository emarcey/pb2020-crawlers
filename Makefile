IMAGE_NAME = "pb2020-content-reader"

READER_MODE = "default"
READER_MODE_REDDIT = "reddit"

JOB_SLEEP_TIME_SECONDS="30"


build:
	docker build --rm \
	--tag=$(IMAGE_NAME) \
	.

run:
	$(MAKE) build
	docker run -it \
	-v=$(CURDIR):/rss_feeds \
	-e READER_MODE=$(READER_MODE) \
	-e JOB_SLEEP_TIME_SECONDS=$(JOB_SLEEP_TIME_SECONDS) \
	$(IMAGE_NAME) \
	$(cmd)

run_reddit:
	$(MAKE) build
	$(MAKE) run READER_MODE=$(READER_MODE_REDDIT)

unit:
	$(MAKE) build
	$(MAKE) run cmd="python -m pytest ./tests/unit/"
