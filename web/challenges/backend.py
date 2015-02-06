import dbus

system_bus = dbus.SystemBus()
daemon = "de.fxrh.ctfserver"
daemon_object = "/CTFServer"


def create_challenge(challenge):
    proxy = system_bus.get_object(daemon, daemon_object)
    proxy.addServiceAccount(challenge.id)


def update_keys_for_user(user):
    proxy = system_bus.get_object(daemon, daemon_object)
    for challenge in user.created_challenges():
        proxy.setServiceKeys(challenge.id, user.ssh_key)