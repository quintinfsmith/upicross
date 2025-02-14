#!/bin/bash

while test $# != 0
do
    case "$1" in
    --local)    python3 setup.py install --prefix $VIRTUAL_ENV/
                rm picross.egg-info -rf
                rm build -rf
                rm dist -rf ;;
    --publish)  python3 setup.py sdist bdist_wheel
                python3 -m twine upload dist/*
                rm picross.egg-info -rf
                rm build -rf
                rm dist -rf ;;
    *) break ;;
    esac
    shift
done

