rmux
====

``rmux`` allows you to run your local project on multiple remote machines in
parallel.

The command names comes from remote-tmux as it allows multiplexing commands
on multiple remote machines, synchronized.

The original purpose was to allow testing local changes to a project on other
platforms, like running tox on another distribution.

![](https://raw.githubusercontent.com/pycontribs/rmux/master/docs/movie.gif)

Usage
-----

```bash
# run df locally
rmux df

# close tmux session
exit

# run df on two remote hosts, syncronized windows
HOSTS="node1 node2" rmux df

# run a script downloaded from the web (installs pip)
rmux -w https://bootstrap.pypa.io/get-pip.py

```

If you fail to define the ``HOSTS`` variable the tool will default to localhost
but it will still use its logic of doing a rsync and running commands using
tmux and ssh.

How it works
------------

``rmux`` will detect current project by looking for the ``.git`` folder
it in current directory or its parents.  If it fails to find
any ``.git`` folder, it will skip the rsync part.

The script will not rsync ``.gitignored`` files but it will sync untracked
files.

The destination folder on remote machines is ``~/.cache/.rmux/<projectname>``
which will also become default directory.

The remote user is based on host names or your ssh configuration.

Installation
------------

```bash
pip install rmux
```

While ``rmux`` is currently only a pure bash script, I used pip wheel as a way
to distribute it as it cross platform and easy to use. In addition, it allows
me to easily upgrade it.

If you prefer you can
just download the shell script and add it to your path.

See also
--------

* [tmux](https://github.com/tmux/tmux/wiki) - terminal multiplexer
* [tmux-xpanes](https://github.com/greymd/tmux-xpanes) - auto-window layout
  for tmux, a current requirement for rmux. Still, it should be possible to
  avoid using it if you have only one remote host, just make a feature request
  and I can implement it.
* [direnv](https://direnv.net/) - define environment variables specific to current directory. This can be very handy if you want to have different set of HOSTS
  for each project and avoid mentioning them on the command line.
* [rtox](https://pypi.org/project/rtox/) which allows running tox on remote
  machines this being the original project. With rmux you will no longer need
  rtox as you can just do `rmux tox` instead of `rtox`, the big difference
  being that the session is not closed automatically and that you can now
  run on multiple remote hosts instead of just one.

Links
-----
* Free software: Apache license
* Source: https://github.com/pycontribs/rmux
* Bugs: https://github.com/pycontribs/rmux/issues
