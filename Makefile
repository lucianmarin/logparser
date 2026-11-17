PURA ?= pura

# Install system-wide when run as root (sudo make install), per-user otherwise.
PREFIX ?= $(if $(filter 0,$(shell id -u)),/usr/local,$(HOME)/.local)
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
