1. Windows 10 [Download Docker for Windows](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe)
2. Windows 7 [Download Docker Toolbox for Windows](https://docs.docker.com/toolbox/overview/#whats-in-the-box)
        a. Install Docker Toolbox with all the defaults
        b. Open Kitematic
        c. Click on Docker CLI at the bottom left of the Kitematic window
        d. cd $home
        e. mkdir src
        f. cd src
        g. git clone https://github.com/pierrerochard/bitcoin-lightning-docker
        h. cd bitcoin-lightning-docker
        i. docker-compose up