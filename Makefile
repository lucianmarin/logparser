PURA ?= pura

PREFIX ?= $(if $(wildcard $(HOME)/.local),$(HOME)/.local,/usr/local)
BINDIR ?= $(DESTDIR)$(PREFIX)/bin

TARGET = logparser
SRC = logparser.pura

.PHONY: all check install uninstall clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(PURA) --compile $(SRC) -o $(TARGET)

check:
	$(PURA) --check $(SRC)

install: $(TARGET)
	install -d "$(BINDIR)"
	install -m 755 $(TARGET) "$(BINDIR)/$(TARGET)"

uninstall:
	rm -f "$(BINDIR)/$(TARGET)"

clean:
	rm -f $(TARGET)
