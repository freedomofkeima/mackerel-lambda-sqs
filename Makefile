BUILDDIR = build/lambda
PWD := $(shell pwd)
lambda.zip:
	mkdir -p $(BUILDDIR)
	cp -a conf.json $(BUILDDIR)
	cp -a handler.py $(BUILDDIR)
	pip install mackerel.client -t $(BUILDDIR)
	touch $(BUILDDIR)/mackerel/__init__.py
	cd $(BUILDDIR); zip -r lambda.zip .
	mv $(BUILDDIR)/lambda.zip .

clean:
	-rm -rf build/
	-rm lambda.zip
