# phpbuild
Need an obscure version of PHP and some extensions? phpbuild is here to help!

## Using
1. Set your `config.yaml` up with the versions of extensions you want. This will
   be merged with a default set of extensions (coming soon); specify `~` (YAML
   null) as the version to not install it.
2. Run `vagrant up` to set up the testing machine
3. ... Coming soon, a working executable!

## Todo
* Parse default versions from `win32/build/libs_version.txt` for the given PHP
  version, using the `default` key for the extension
