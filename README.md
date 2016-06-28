Talos-Flask
===========

Takes the Talos automated theorem prover and provides a flask wrapper around it so that it could be run as a web service.

This application relies on one dependency (that in turn has its own dependency) that are included as git submodules:

* [Talos](https://github.com/RAIRLab/Talos)
* [DCEC_Library](https://github.com/RAIRLab/DCEC_Library)

When closing this repository, you must also clone these submodules or else this will fail to run properly.


If you wish to use this repository, you need to run the following command:
```
git clone --recursive https://github.com/RAIRLab/Talos-Flask
```
which will give you both the repository and its associated submodules.


Included additionally are files in putting this repository on the IBM BlueMix platform.