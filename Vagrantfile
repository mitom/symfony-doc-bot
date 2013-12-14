Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu-raring64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/raring/current/raring-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.network "private_network", ip: "192.168.100.2"
  config.vm.synced_folder ".", "/vagrant", nfs: true

  config.vm.provision :shell, :path => "vagrant/scrapy.sh"
  config.vm.provision :shell, :path => "vagrant/elasticsearch.sh"
  config.vm.provision :shell, :path => "vagrant/cloudbot.sh"
end
