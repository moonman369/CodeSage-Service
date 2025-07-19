@echo off
setlocal enabledelayedexpansion

:: Fun header
echo ============================================================
echo   🚀 CodeSage Test Workflow Launcher 🚀
echo ============================================================
echo.

:: Progress bar function
set "bar=##################################################"
set "barlen=50"

:: Function to show progress bar
set show_progress=for /l %%i in (1,1,%barlen%) do (
    set /a percent=%%i*2
    set "progress=!bar:~0,%%i!"
    <nul set /p="    [!progress!]"
    timeout /t 1 >nul
    <nul set /p=" %percent%%%`r"
)
:: Step 1: Run digestor tests
echo Step 1/5: Running unit tests...
call :progress_bar
python -m test.digestor.repomix_digestor_test
if %errorlevel% neq 0 (
    echo ❌ Digestor test failed!
    goto end
) else (
    echo ✅ Digestor tests passed!
)
echo.

:: Step 2: Run chunk processor test
echo Step 2/5: Running chunk processor test...
call :progress_bar
python -m test.chunker.test_basic_chunker
if %errorlevel% neq 0 (
    echo ❌ Digestor test failed!
    goto end
) else (
    echo ✅ Digestor tests passed!
)
echo.

:: Step 3: Run summarizer test
echo Step 3/5: Running summarizer test...
call :progress_bar
python -m test.summarizer.test_chunk_processor
if %errorlevel% neq 0 (
    echo ❌ Summarizer test failed!
    goto end
) else (
    echo ✅ Summarizer test passed!
)
echo.

:: Step 4: Run embedder test
echo Step 4/5: Running embedder test...
call :progress_bar
python -m test.embedder.test_local_embedder
if %errorlevel% neq 0 (
    echo ❌ Embedder test failed!
    goto end
) else (
    echo ✅ Embedder test passed!
)
echo.

:: Step 5: Run Vector Store test
echo Step 5/5: Running vector store test...
call :progress_bar
python -m test.vector_store.test_qdrant_vector_store
if %errorlevel% neq 0 (
    echo ❌ Vector Store test failed!
    goto end
) else (
    echo ✅ Vector Store test passed!
)
echo.

:: Fun finish
echo ============================================================
echo   🎉 All tests completed! You're a CodeSage Wizard! 🧙‍♂️
echo ============================================================
goto end

:: Progress bar subroutine
:progress_bar
setlocal enabledelayedexpansion
set "bar=##################################################"
set "barlen=50"
<nul set /p="    ["
for /l %%i in (1,1,%barlen%) do (
    set /a percent=%%i*2
    set "progress=!bar:~0,%%i!"
    <nul set /p="#"
    ping -n 1 127.0.0.1 >nul
)
<nul set /p="] 100%%"
echo.
endlocal
goto :eof

:end
endlocal
pause