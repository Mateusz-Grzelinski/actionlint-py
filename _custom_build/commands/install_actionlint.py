from setuptools import Command


class install_actionlint(Command):
    description = "install the actionlint executable"
    outfiles = ()
    build_dir = install_dir = None
    user_options: "list[tuple]" = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        # this initializes attributes based on other commands' attributes
        self.set_undefined_options("build", ("build_temp", "build_dir"))
        self.set_undefined_options(
            "install",
            ("install_scripts", "install_dir"),
        )

    def run(self):
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)

    def get_outputs(self):
        return self.outfiles
