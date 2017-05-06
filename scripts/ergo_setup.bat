rem This script sets up Ergonomica.

cd %UserProfile%

if exist .ergo (
    echo %UserProfile%\.ergo already exists.
) else (
    mkdir .ergo
    echo Created %UserProfile%\.ergo.
    cd .ergo
    mkdir packages
    echo Created %UserProfile%\.ergo\packages.
    copy NUL .ergo_profile
    echo Created %UserProfile%\.ergo\.ergo_profile.
    copy NUL .ergo_history
    echo Created %UserProfile%\.ergo\.ergo_history.
    echo All files created successfully.
)

pause
