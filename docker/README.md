# README #

## TL;DR version ##
1. Run the dockers

        ./docker/run_dockers.bsh
        
2. **Enjoy** all your new package files in

        ./repos/
        
## Using the Dockers ##

All docker commands need to either be run as root **or** as a user with docker 
permissions. Adding your user name to the docker group (or setting up boot2docker 
environment) is probably the easiest.

For Mac and Windows users, the git-lfs repo needs to be in your Users directory 
or else boot2docker magic won't work. Alternatively, you could add addition
mount points like 
[this](http://stackoverflow.com/questions/26639968/boot2docker-startup-script-to-mount-local-shared-folder-with-host)

### Running Dockers ###

In order to run the dockers, the docker has to be run with a
lot of arguments to get the mount points right, etc... A convenient script is 
supplied to make this all easy. Simply run

    ./docker/run_docker.bsh
    
All the images are pulled automatically, and then run.

To only run certain docker images, supply them as arguments, e.g.

    ./docker/run_docker.bsh debian_7
    ./docker/run_docker.bsh centos_7 debian_8
    ./docker/run_docker.bsh centos_{5,6,7}

And only those images will be run.

### Development in Dockers ###

Sometimes you don't want to just build git-lfs and destroy the container, you
want to get in there, run a lot of command, debug, develop, etc... To do this, 
the best command to run is bash, and then you have an interactive shell to use

    ./docker/run_docker.bsh {image name(s)} -- bash

After listing the image(s) you want to run, add a double dash (--) and then any 
command (and arguments) you want executed in the docker. Remember, the command
you are executing has to be in the docker image.

## Docker images ##

Build images are named `{OS NAME}_{OS VERSION}` - These build
git-lfs and save the package/repository in the `/repo` direrctory. This image
also signs all rpms/debs if gpg signing is setup

This default behavior for `./docker/run_dockers.bsh`
is to run all of the _build images_. These
containers will use the currently checked-out version of git-lfs and copy it 
into the docker, and run `git clean -xdf` to remove any non-tracked files, 
(but non-committed changes are kept). git-lfs is built, and a packages is 
created for each container.

These are all a developer would need to test the different OSes. And create the
git-lfs rpm or deb packages in the `/repo` directory. 

### Run Docker Environment Variables ###

There are a few environment variables you can set to easily adjust the behavior
of the `run_docker.bsh` script.

`export` before calling `run_docker.bsh`

`DOCKER_AUTOPULL` - Default 1. `run_docker.bsh` always pulls the latest version of
the lfs dockers. If set to 0, it will not check to see if a new pull is needed,
and you will always run off of your currently cached images docker images.

`AUTO_REMOVE` - Default 1. Docker containers are automatically deleted on 
exit. If set to 0, the docker containers will not be automatically deleted upon 
exit. This can be useful for a post mortem analysis (using other docker commands
not covered here). Just make sure you clean up the docker containers manually.

`DOCKER_OTHER_OPTIONS` - Any additional arguments you may want to pass to the
docker run command. This can be particularly useful when having to help docker
with dns, etc... For example `DOCKER_OTHER_OPTIONS="--dns 8.8.8.8"`

If for some reason on Windows, you need to add a -v mount, folder names need to
start with `//driveleter/dir...` instead of `/driveleter/dir...` to fool MINGW32

## Adding additional OSes ##

To add another operating system, it needs to be added to the lfs_dockers 
repo and uploaded to docker hub. Then all that is left is to add it to the 
IMAGES list in `run_dockers.bsh`

Follow the already existing pattern `{OS NAME}_{OS VERSION #}` where 
**{OS NAME}** and **{OS VERSION #}** should not contain underscores (\_).

## Docker Cheat sheet ##

Install https://docs.docker.com/installation/

* list running dockers

    docker ps
    
* list stopped dockers too

    docker ps -a
    
* Remove all stopped dockers

    docker rm $(docker ps --filter=status=exited -q)
    
* List docker images

    docker images

* Remove unused docker images

    docker rmi $(docker images -a --filter=dangling=true -q)
    
* Run another command (like bash) in a running docker

    docker exec -i {docker name} {command}

* Stopping a docker (signal 15 to the main pid)

    docker stop {docker name}

* Killing a docker (signal 9 to the main pid)

    docker kill {docker name}

# Troubleshooting #

1. I started one of the script, and am trying to stop it with Ctrl+C. It is
ignoring many Ctrl+C's

    This happens a lot when calling programs like apt-get, yum, etc... From the
    host, you can still use ps, pgrep, kill, pkill, etc... commands to kill the
    PIDs in a docker. You can also use `docker ps` to find the container
    name/id and then used `docker stop` (signal 15) or `docker kill`
    (signal 9) to stop the docker. You can also use 'docker exec' to start another
    bash or kill command inside that container
    
2. How do I re-enter a docker after it failed/succeeded?

    Dockers are immediately deleted upon exit. The best way to work in a docker
    is to run bash (See Development in Dockers). This will let you to run the 
    main build command and then continue.
    
3. That answer's not good enough. How do I resume a docker?

    Well, first you have to set the environment variable `AUTO_REMOVE=0` 
    before running the image you want to resume. This will keep the docker 
    around after stopping. (Be careful! They multiply like rabbits.) Then
    
        docker commit {container name/id} {new_name}
    
    Then you can `docker run` that new image.
