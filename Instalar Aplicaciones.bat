:: ===============================
:: ======== Instalar Code ========
:: ===============================

winget install -e --id Microsoft.VisualStudioCode

:: ===============================
:: ======= Instalar Python =======
:: ===============================

winget install -e --id Python.Python.3.11

:: ===============================
:: ======= Instalar Github =======
:: ===============================

winget install -e --id GitHub.GitHubDesktop

:: ===============================
:: ==== Instalar Extensiones =====
:: ===============================

cmd /C code --install-extension donjayamanne.python-extension-pack
cmd /C code --install-extension batisteo.vscode-django
cmd /C code --install-extension qwtel.sqlite-viewer

pause