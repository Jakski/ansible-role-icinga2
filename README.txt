ansible-role-icinga2
********************

Ansible role to setup Icinga2 cluster


Variables
=========

icinga2_service

   System service name

icinga2_master

   Master node with ability to sign client certificates

icinga2_packages

   Packages with Icinga2

icinga2_default_release

   Default packages release

icinga2_state

   Desired service state

icinga2_enabled

   Whether to enable system service

icinga2_restart

   Whether to restart when necessary

icinga2_reload

   Whether to reload when necessary

icinga2_conf_template

   Main configuration file template

icinga2_user

   User for service and file system permissions

icinga2_group

   Group for service and file system permissions

icinga2_conf_includes

   Configuration includes

icinga2_conf_recursive_includes

   Recursive configuration includes

icinga2_data_dir

   Data directory

icinga2_conf_dir

   Configuration directory

icinga2_constants

   Configuration constants

icinga2_conf_extra

   Custom Icinga2 main configuration fragment

icinga2_features

   Features configuration

icinga2_manage_features

   Whether to disable unmanaged features

icinga2_ca_cert

   CA certificate

icinga2_ca_key

   CA key

icinga2_client_cert

   Client certificate

icinga2_client_key

   Client certificate key

icinga2_manage_conf

   Whether to manage files in scripts, zones and objects directory

icinga2_scripts_dir

   Directory with scripts

icinga2_objects_dir

   Directory with objects configuration

icinga2_objects_conf

   Objects configuration files

icinga2_zones

   Zones

icinga2_scripts

   Scripts


Examples
========

   ---
   - hosts: "master-{{ lookup('env', 'MOLECULE_INSTANCE_SUFFIX') | default('instance', true) }}"
     vars:
       role_defaults: "{{ lookup('file', role_path + '/defaults/main.yml') | from_yaml }}"
       objects:
         host2: |
           object Host "host2" {
             import "generic-host"
             address = "127.0.0.1"
           }
     tasks:
       - name: Install HTTPS transport for APT
         apt:
           name: apt-transport-https
           state: "present"

       - name: Add repository key
         apt_key:
           id: "F51A91A5EE001AA5D77D53C4C6E319C334410682"
           data: "{{ lookup('file', 'repository.key') }}"
           state: "present"

       - name: Add repository source
         apt_repository:
           repo: "{{ item }}"
           filename: "icinga2"
           update_cache: true
           state: "present"
         loop:
           - "deb https://packages.icinga.com/debian icinga-{{ ansible_facts.distribution_release }} main"
           - "deb-src https://packages.icinga.com/debian icinga-{{ ansible_facts.distribution_release }} main"

       - import_role:
           name: icinga2
         vars:
           icinga2_features: "{{ role_defaults.icinga2_features | combine({'api': None}) }}"
           icinga2_zones:
             test3.local:
               hosts: |
                 object Host "host1" {
                   import "generic-host"
                   address = "127.0.0.1"
                 }
               groups: |
                 object HostGroup "freebsd-servers" {
                   display_name = "FreeBSD"
                   assign where host.vars.os == "FreeBSD"
                 }
           icinga2_objects_conf: "{{ role_defaults.icinga2_objects_conf | combine(objects) }}"


Documentation
=============

Compile:

   $ pip3 install -r requirements.txt
   $ make man

View:

   $ man ./docs/man/ansible-role-icinga2.1
