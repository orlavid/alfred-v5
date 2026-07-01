.PHONY: review test status

review:
	python build_executive_review.py
	cat output/Executive_Review.md

test:
	python -m tests.test_executive_review

status:
	git status
	git log --oneline --decorate -8
