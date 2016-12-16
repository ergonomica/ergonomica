rem This script sets up Ergonomica.

cd

if exist .ergo (
    echo .ergo already exists.
) else (
    mkdir .ergo
    echo Created .ergo.
    cd .ergo
    mkdir packages
    echo Created .ergo/packages.
    copy NUL .ergo_profile
    echo Created .ergo/.ergo_profile.
    copy NUL .ergo_history
    echo Created .ergo/.ergo_history.
    echo All files created successfully.
)

pause
