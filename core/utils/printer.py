from tabulate import tabulate
from core.utils.helpers import Helpers

class Printer:
    def __init__(self, args):
        self.args = args

    def print(self, data):
        if self.args.username:
            for i in data:
                self.print_user(i)
        elif self.args.organization:
            for i in data:
                self.print_organization(i)
        else:
            self.print_repos([data])
        return True

    def print_organization(self, organization):
        base = "[+] {}".format(organization.name)
        if organization.email:
            base = "{} <{}>".format(base, organization.email)
        if organization.members:
            base = "{} ({} Members)".format(base, len(organization.members))
        print("{}:".format(base))
        if organization.blog:
            print("  Blog: {}".format(organization.blog))
        self.print_repos(organization.repositories)

    def print_user(self, user):
        base = "[+] {} ({})".format(user.name, user.username)
        if user.email:
            base = "{} - {}".format(base, user.email)
        print("{}:".format(base))
        if user.bio:
            print("  Bio: {}".format(user.bio))
        self.print_repos(user.repositories)

    def print_repos(self, repos, indentation=0):
        if not repos:
            Helpers().print_error(self.indent("No repositories", (indentation + 4)))
        for repo in repos:
            self.print_repo(repo, indentation=(indentation + 4))
            self.print_authors(repo.authors, indentation=(indentation + 8))

    def print_repo(self, repo, indentation=0):
        print(self.indent("- {} ({}):".format(repo.name, repo.url), indentation))

    def print_authors(self, authors, headers=[], table="plain", indentation=0):
        authors_table = [[author.name, author.email] for author in authors]
        print(self.indent(tabulate(authors_table, headers, table), indentation))

    def indent(self, txt, spaces=4):
        return "\n".join("{}{}".format(" "*spaces, ln) for ln in txt.splitlines())
