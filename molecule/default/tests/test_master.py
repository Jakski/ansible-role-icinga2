import os

from testinfra.utils.ansible_runner import AnsibleRunner
from pytest import fixture


@fixture
def master_instance():
    inventory = os.environ['MOLECULE_INVENTORY_FILE']
    host = 'master-' + os.environ.get('MOLECULE_INSTANCE_SUFFIX', 'instance')
    return AnsibleRunner(inventory).get_host(host)


def test_master_service(master_instance):
    assert master_instance.service('icinga2').is_running
    assert master_instance.socket('tcp://0.0.0.0:5665').is_listening


def test_master_configuration(master_instance):
    main_cfg = master_instance.file('/etc/icinga2/icinga2.conf')
    assert main_cfg.contains('^const ZoneName = "master-instance"$')
    assert main_cfg.user == 'nagios'
    assert main_cfg.group == 'nagios'
    assert main_cfg.mode == 0o640

    assert master_instance.file(
        '/etc/icinga2/zones.d/test3.local/groups.conf').contains('FreeBSD')
    assert master_instance.file(
        '/etc/icinga2/zones.d/test3.local/local/hosts.conf').contains('host1')
    assert master_instance.file(
        '/etc/icinga2/conf.d/local/host2.conf').contains('host2')


def test_master_features(master_instance):
    enabled = master_instance.check_output(
        'icinga2 feature list').split('\n')[1].split()[2:]
    assert 'api' in enabled
    assert 'checker' in enabled
    assert 'mainlog' in enabled
    assert 'notification' in enabled


def test_master_unmanaged_configuration(master_instance):
    files = [
        'conf.d/hosts/host1.conf',
        'conf.d/hosts/host2.conf',
        'conf.d/groups/group1.conf',
        'conf.d/groups/group2.conf',
        'conf.d/app2.conf',
        'conf.d/notifications2.conf',
        'zones.d/test1.local/groups.conf',
        'zones.d/test1.local/local/hosts/host1.conf',
        'zones.d/test2.local/groups.conf',
        'zones.d/test2.local/hosts.conf',
    ]
    for file in files:
        assert not master_instance.file('/etc/icinga2/' + file).exists
