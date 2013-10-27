# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
	# All Vagrant configuration is done here. The most common configuration
	# options are documented and commented below. For a complete reference,
	# please see the online documentation at vagrantup.com.

	# Every Vagrant virtual environment requires a box to build off of.
	config.vm.box = "precise32"

	# The url from where the 'config.vm.box' box will be fetched if it
	# doesn't already exist on the user's system.
	# config.vm.box_url = "http://domain.com/path/to/above.box"

	# Create a forwarded port mapping which allows access to a specific port
	# within the machine from a port on the host machine. In the example below,
	# accessing "localhost:8080" will access port 80 on the guest machine.
	# config.vm.network :forwarded_port, guest: 80, host: 8080

	# Create a private network, which allows host-only access to the machine
	# using a specific IP.
	# config.vm.network :private_network, ip: "192.168.33.10"

	# Create a public network, which generally matched to bridged network.
	# Bridged networks make the machine appear as another physical device on
	# your network.
	# config.vm.network :public_network

	config.vm.provision :shell, :inline => "apt-get update"

	config.vm.provision :puppet do |puppet|
		puppet.manifests_path = "vagrant/puppet/manifests"
		puppet.module_path    = "vagrant/puppet/modules"
		puppet.manifest_file  = "init.pp"
		puppet.options = "--debug --verbose"
	end

	# Enable provisioning with chef solo, specifying a cookbooks path, roles
	# path, and data_bags path (all relative to this Vagrantfile), and adding
	# some recipes and/or roles.
	#
	# config.vm.provision :chef_solo do |chef|
	#   chef.cookbooks_path = "../my-recipes/cookbooks"
	#   chef.roles_path = "../my-recipes/roles"
	#   chef.data_bags_path = "../my-recipes/data_bags"
	#   chef.add_recipe "mysql"
	#   chef.add_role "web"
	#
	#   # You may also specify custom JSON attributes:
	#   chef.json = { :mysql_password => "foo" }
	# end

	# Enable provisioning with chef server, specifying the chef server URL,
	# and the path to the validation key (relative to this Vagrantfile).
	#
	# The Opscode Platform uses HTTPS. Substitute your organization for
	# ORGNAME in the URL and validation key.
	#
	# If you have your own Chef Server, use the appropriate URL, which may be
	# HTTP instead of HTTPS depending on your configuration. Also change the
	# validation key to validation.pem.
	#
	# config.vm.provision :chef_client do |chef|
	#   chef.chef_server_url = "https://api.opscode.com/organizations/ORGNAME"
	#   chef.validation_key_path = "ORGNAME-validator.pem"
	# end
	#
	# If you're using the Opscode platform, your validator client is
	# ORGNAME-validator, replacing ORGNAME with your organization name.
	#
	# If you have your own Chef Server, the default validation client name is
	# chef-validator, unless you changed the configuration.
	#
	#   chef.validation_client_name = "ORGNAME-validator"
end
