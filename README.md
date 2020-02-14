# Password Locker (*passlock*)
> *Encrypt your passwords from prying eyes.*

![Python version][python-version]
![Latest version][latest-version]
[![GitHub issues][issues-image]][issues-url]
[![GitHub forks][fork-image]][fork-url]
[![GitHub Stars][stars-image]][stars-url]
[![License][license-image]][license-url]

NOTE: This project was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with [@clamytoe's](https://github.com/clamytoe) [toepack](https://github.com/clamytoe/toepack) project template.

### Initial setup
```zsh
(base) ➜  ~ cd Projects
(base) ➜  Projects git clone https://github.com/clamytoe/passlock.git
(base) ➜  Projects cd passlock
```

#### Anaconda setup
If you are an Anaconda user, this command will get you up to speed with the base installation.
```zsh
(base) ➜  passlock git:(master) conda env create
(base) ➜  passlock git:(master) conda activate passlock
```

#### Regular Python setup
If you are just using normal Python, this will get you ready, but I highly recommend that you do this in a virtual environment. There are many ways to do this, the simplest using *venv*.
```zsh
(base) ➜  passlock git:(master) python3 -m venv venv
(base) ➜  passlock git:(master) source venv/bin/activate
(passlock) ➜  passlock git:(master) pip install -r requirements.txt
```

#### Final setup
```zsh
(passlock) ➜  passlock git:(master) pip install -e .
```

## Usage
At the moment I just have a sample entry so simply running the command will demonstrate what it does. 

```zsh
(passlock) ➜  passlock git:(master) passlock
Successfully created: /home/mohh/Documents/.passlock/ip.bin

[ip]
INFO: http://192.168.2.1
USER: admin
PASS: admin
```

The encrypted file will be created in `~/Documents/.passlock/ip.bin` and it's contents will look something like this:

```text
�.z����dz�L���6��-`b
                     �
                      ZP�ɚO���Bg���4���7e�ܧ��T�GH�:B��������b��/5����@��PH�Gp��>xi���q��@�(pWb%��Ǜ�9UE���W���m����hN���� D$�f����_��"z��M
                                                                  �p�T�|
�T���`��m6p�"/E���>+�h���d/'H����E�RRBƞ��a�A�[#�
                   �Ɖ�I��۞����i6�'cZH;��ݢN
%�y?@~�Dz�,��Og)�
+����ن���ߺ��`�	5	LC��S��1������{M�F	PW��0Q�����Ǒ�������Ƌ��ߕ���pb�/E��$�8�]`������I)�#c���X4�
                               w�fb�M���g�A[gYZ�étk�dg�'���;��D	�t�_��JHW�J~��)G�}}��/N�jD��W���[0���7g��u�8OO�ǿP02n�y����%ׄ_��+^_Le��Z�x��fD�6+h;�6���2C����OXJl$�h���%  
```

At the same time, it will generate a new private and public keys for the program and stash them in `~/.passloc/`.

> **NOTE**: At this time, you must run the `passlock` command from within the project folder. I'm working on how to update the path for the log files dynamically during the project creation. 
## TODO
* Setup path for logging during package creation
* Add a CLI interface that will:
    * List all entries
    * Search for a particular entry
    * Add/Update and entry
    * Remove and entry
    * Export all data
* Add a GUI that does the same as the CLI

## Contributing
Contributions are very welcome. Tests can be run with with `pytest -v`, please ensure that all tests are passing and that you've checked your code with the following packages before submitting a pull request:
* black
* isort
* mypy
* pytest-cov

I am not adhering to them strictly, but try to clean up what's reasonable.

## License
Distributed under the terms of the [MIT](https://opensource.org/licenses/MIT) license, "passlock" is free and open source software.

## Issues
If you encounter any problems, please [file an issue](https://github.com/clamytoe/toepack/issues) along with a detailed description.

## Changelog
* **v0.1.4** Added extensive logging.
* **v0.1.3** Moved Entity and Vault classes into their own files.
* **v0.1.2** Added Entity class to encrypt independent entries.
* **v0.1.1** Created Vault class to encrypt files.
* **v0.1.0** Initial commit.

[python-version]:https://img.shields.io/badge/python-3.8-brightgreen.svg
[latest-version]:https://img.shields.io/badge/version-0.1.0-blue.svg
[issues-image]:https://img.shields.io/github/issues/clamytoe/passlock.svg
[issues-url]:https://github.com/clamytoe/passlock/issues
[fork-image]:https://img.shields.io/github/forks/clamytoe/passlock.svg
[fork-url]:https://github.com/clamytoe/passlock/network
[stars-image]:https://img.shields.io/github/stars/clamytoe/passlock.svg
[stars-url]:https://github.com/clamytoe/passlock/stargazers
[license-image]:https://img.shields.io/github/license/clamytoe/passlock.svg
[license-url]:https://github.com/clamytoe/passlock/blob/master/LICENSE
