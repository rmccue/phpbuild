package { [ "python2.7", "python2.7-dev", "git", "make", "cmake" ]:
	ensure => latest,
}

package {"python-pip":
	require => Package["python2.7"],

	ensure => latest,
}

# Fetch libgit2
vcsrepo { '/usr/src/libgit2':
	require => Package["git"],

	ensure   => present,
	provider => git,
	source   => 'https://github.com/libgit2/libgit2.git',
	revision => "v0.19.0",
}

file { "/usr/src/libgit2/build":
	require => Vcsrepo["/usr/src/libgit2"],
	ensure => directory
}

# And build it
exec {"libgit2 cmake pre":
	require => File['/usr/src/libgit2/build'],

	command => "/usr/bin/cmake ..",
	cwd => "/usr/src/libgit2/build",
}
exec {"libgit2 cmake build":
	require => Exec["libgit2 cmake pre"],

	command => "/usr/bin/cmake --build .",
	cwd => "/usr/src/libgit2/build",
}
exec { "libgit2 cmake install":
	require => Exec["libgit2 cmake build"],

	command => "/usr/bin/cmake --build . --target install",
	cwd => "/usr/src/libgit2/build",
}

exec { "pip install -r requirements.txt":
	require => [ Package["python-pip"], Package["python2.7-dev"], Exec["libgit2 cmake install"] ],

	cwd => "/vagrant",
	path => "/usr/bin",
}

# PHP build requirements
package { [ "autoconf", "bison", "libtool", "re2c", "flex" ]:
	ensure => installed,
}

# Default extension requirements
# TODO: handle these in phpbuild instead
package { [ "libxml2-dev" ]:
	ensure => installed,
}
