CC = gcc
FLEX = flex

# Flex source file
LEXER_SRC = lexer.l
# Generated C source
LEXER_C = lex.yy.c
# Output executable
TARGET = lexer.exe

all: $(TARGET)

$(TARGET): $(LEXER_C)
	$(CC) -o $@ $^ -lfl

$(LEXER_C): $(LEXER_SRC)
	$(FLEX) $<

clean:
	rmdir /S /Q __pycache__ 2>nul || echo No __pycache__
	del /F /Q $(LEXER_C) $(TARGET) 2>nul || echo No generated files
