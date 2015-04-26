import dbus

daemon = "de.fxrh.ctfserver"
daemon_object = "/CTFServer"


def create_challenge(challenge, user):
    system_bus = dbus.SystemBus()
    proxy = system_bus.get_object(daemon, daemon_object)
    proxy.addServiceAccount(challenge.id)
    if user.ssh_key != "":
        proxy.setServiceKeys(challenge.id, user.ssh_key)


def update_keys_for_user(user):
    system_bus = dbus.SystemBus()
    proxy = system_bus.get_object(daemon, daemon_object)
    for challenge in user.created_challenges():
        proxy.setServiceKeys(challenge.id, user.ssh_key)