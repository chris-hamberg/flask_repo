'''
Automate a github repository for flask projects.

    - create the local repo
    - create the remote repo
    - pull flask_base
'''
from config import user, workspace
import argparse, json, logging, os


logging.basicConfig(level=logging.INFO, format=' ~$ %(message)s')


class Repository:

    def __init__(self):
        self.parse()
        self.dest = os.path.join(os.environ['HOME'], workspace, self.repo)
        self.remote_ssh = f'git@github.com:{self.user}/{self.repo}.git'
        self.flask_base = f'git@github.com:{self.user}/flask_base.git'

    def delegate(self):
        self.create_workspace()
        self.create_remote()
        self.create_local()

    def parse(self):
        parser = argparse.ArgumentParser(
            description = 'Create a new local & remote repo from flask base template'
        )
        parser.add_argument('--repo', '-r', help='new repo name', required=True)
        parser.add_argument('--user', '-u', default=user, help='github user name')
        args = parser.parse_args()
        self.user = args.user
        self.repo = args.repo

    def create_workspace(self):
        if not os.path.exists(self.dest):
            os.mkdir(self.dest)
        os.chdir(self.dest)

    def create_local(self, test=False):
        commands = [
        'git init',
        f'git remote add origin {self.flask_base}',
        'git pull origin master',
        'git remote remove origin',
        f'git remote add origin {self.remote_ssh}',
        'git add .', 
        'git commit -am "init"',
        'git push -u origin master'
        ]
        for command in commands:
            if test:
                logging.info(command)
            else:
                os.system(command)
        if not test:
            os.system('tree')

    def create_remote(self, test=False):
        repo = json.dumps({'name': self.repo})
        url = 'https://api.github.com/user/repos'
        command = f"curl -u '{self.user}' {url} -d '{repo}'"
        if test:
            logging.info(command)
        else:
            os.system(command)

if __name__ == '__main__':
    repo = Repository()
    #repo.create_local(True)
    #repo.create_remote(True)
    repo.delegate()