@echo off
setlocal
echo Este comando baixa o modelo qwen3:1.7b para a comparacao academica.
echo O download usa a internet e ocupa espaco no computador.
pause
ollama pull qwen3:1.7b
if errorlevel 1 (
    echo Falha no download. Confirme se o Ollama esta instalado e conectado.
    pause
    exit /b 1
)
echo Segundo modelo instalado. Execute executar_avaliacao_completa.bat.
pause
endlocal
