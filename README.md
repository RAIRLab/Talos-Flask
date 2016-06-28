Talos-Flask
===========

Takes the Talos automated theorem prover and provides a flask wrapper around it so that it could be run as a web service.

This application relies on two dependencies that are included as submodules (and then from there, SPASS must be compiled as well):

* [Talos](https://github.com/RAIRLab/Talos)
* [DCEC_Library](https://github.com/RAIRLab/DCEC_Library)

These are included in the project as git submodules inside this repository.


If you wish to use this repository, you need to run the following command:
```
git clone --recursive https://github.com/RAIRLab/Talos-Flask
```
which will give you both the repository and its associated submodules.


Included are files in hosting this repository on the IBM BlueMix platform.