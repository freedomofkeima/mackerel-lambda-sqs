BUILDDIR = build/lambda
PWD := $(shell pwd)
lambda.zip:
	mkdir -p $(BUILDDIR)
	cp -a conf.json $(BUILDDIR)
	cp -a handler.py $(BUILDDIR)
	pip install mackerel.clienthde -t $(BUILDDIR)
	cd $(BUILDDIR); zip -r lambda.zip .
	mv $(BUILDDIR)/lambda.zip .

clean:
	-rm -rf build/
	-rm lambda.zip
