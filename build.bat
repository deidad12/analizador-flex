@echo off
rem Build the Flex lexer on Windows

flex lexer.l
if errorlevel 1 (
  echo Flex failed
  exit /b 1
)

gcc -o lexer.exe lex.yy.c
if errorlevel 1 (
  echo gcc failed
  exit /b 1
)

echo Build succeeded
