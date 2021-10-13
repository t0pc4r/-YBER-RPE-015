from ...module import Module

class SSHModule(Module):

    def get_labeler_name(self):
        return "ssh_labeler"

    def get_topic(self):
        return "ssh"

    def get_query(self):
        return {
            "ips": self.module_config["ips"]
        }
        