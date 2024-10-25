POST_DIRS := $(shell find ./staging/* -maxdepth 0 -type d -not -path "./staging/content*")

HTML := $(patsubst %, /%.html, $(notdir $(POST_DIRS)))
HTML_FILES := $(join $(POST_DIRS), $(HTML))

PUB := $(patsubst %, /%.status, $(notdir $(POST_DIRS)))
PUB_FILES := $(join $(POST_DIRS), $(PUB))

TEMP_FILES = $(foreach post_dir, $(POST_DIRS), $(wildcard $(post_dir)/_*))

.PHONY: all clean

all: $(PUB_FILES)

%.html:
	@$(MAKE) -C $(dir $@) -f ../../Makefile.convert TARGET=$(notdir $@) NOTEBOOK=$(notdir $(basename $@))

%.status: %.html
	@$(MAKE) -C $(dir $@) -f ../../Makefile.publish TARGET=$(notdir $@) NOTEBOOK=$(notdir $(basename $@))

clean:
	@rm -f $(TEMP_FILES)

publish: $(META)	

define publish-post = 
	@echo publishing $<
endef

$(META) : %.json : %.html
	$(publish-post)
