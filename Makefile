.PHONY: all data preprocess analysis report clean

all: data preprocess analysis report

data:
	python -m src.download_data || python -m src.make_offline_data

preprocess:
	python -m src.preprocess

analysis:
	python -m src.run_all

report:
	python -m src.build_report

clean:
	find figures -name '*.png' ! -name 'banner.png' -delete
	find figures -name '*.svg' ! -name 'banner.svg' -delete
	rm -f tables/*.csv tables/*.md
	rm -f data/processed/*.csv report/report.pdf
